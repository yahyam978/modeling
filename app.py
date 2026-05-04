import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="CHE 3015 — Week 10 Visual Explainer",
    page_icon="⚗️",
    layout="wide",
)

# ── Shared style helpers ─────────────────────────────────────────────────────
BLUE   = "#378ADD"
AMBER  = "#EF9F27"
TEAL   = "#1D9E75"
CORAL  = "#D85A30"
PURPLE = "#7F77DD"
GRAY   = "#888780"

st.markdown("""
<style>
  .formula-box {
    background: #f5f5f0;
    border-left: 4px solid #378ADD;
    border-radius: 6px;
    padding: 10px 16px;
    font-family: monospace;
    font-size: 15px;
    margin: 8px 0 14px;
    color: #1a1a1a;
  }
  .badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 6px;
  }
  .badge-blue  { background:#dbeafe; color:#1e40af; }
  .badge-amber { background:#fef3c7; color:#92400e; }
  .badge-green { background:#d1fae5; color:#065f46; }
  .summary-card {
    background: #f9f9f7;
    border: 1px solid #e2e0d8;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
  }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("⚗️ CHE 3015 — Week 10")
st.sidebar.caption("Second-order systems & linearization")
section = st.sidebar.radio(
    "Jump to section",
    [
        "1 · What is a 2nd-order system?",
        "2 · Bode plot (AR & phase)",
        "3 · Peak AR & corner frequency",
        "4 · Steady-state gain & potential value",
        "5 · Linearization",
        "6 · Worked example — Manometer",
    ],
)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — What is a 2nd-order system?
# ═══════════════════════════════════════════════════════════════════════════════
if section == "1 · What is a 2nd-order system?":
    st.title("What is a second-order system?")
    st.markdown("""
    <div class="summary-card">
    🚗 <b>Think of a car suspension.</b> When you hit a bump, the car bounces.
    How it bounces depends on two things: how stiff the spring is, and how good
    the shock absorber is. A second-order system works exactly the same way.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Natural frequency ωₙ")
        st.markdown("""
        <div class="formula-box">ωₙ = √(2g / L)   ← for a manometer</div>
        """, unsafe_allow_html=True)
        st.write("How fast the system oscillates on its own with no damping — like the natural bounce rate of a spring.")

    with col2:
        st.subheader("Damping ratio δ")
        st.markdown("""
        <div class="formula-box">
        δ &lt; 1 → underdamped (bouncy)<br>
        δ = 1 → critically damped (fastest settle)<br>
        δ &gt; 1 → overdamped (sluggish)
        </div>
        """, unsafe_allow_html=True)
        st.write("How quickly oscillations die out. Controls the shape of the response.")

    st.subheader("Transfer function")
    st.markdown("""
    <div class="formula-box">
    G(s) = ωₙ² / (s² + 2δωₙs + ωₙ²)
    </div>
    """, unsafe_allow_html=True)
    st.write("Put any input in → get the output. The two key parameters are always **δ** and **ωₙ**.")

    # ── Step response comparison ─────────────────────────────────────────────
    st.subheader("Step response — how each damping case looks")
    t = np.linspace(0, 15, 500)
    wn = 1.0

    fig = go.Figure()
    cases = [
        (0.1, BLUE,   "δ = 0.1  underdamped", "dash"),
        (0.3, TEAL,   "δ = 0.3  underdamped", "dot"),
        (0.7, AMBER,  "δ = 0.7  near critical","dashdot"),
        (1.0, CORAL,  "δ = 1.0  critically damped", "solid"),
        (2.0, PURPLE, "δ = 2.0  overdamped",   "longdash"),
    ]

    for delta, color, name, dash in cases:
        wd = wn * np.sqrt(abs(1 - delta**2))
        if delta < 1:
            y = 1 - np.exp(-delta*wn*t)*(np.cos(wd*t) + (delta/np.sqrt(1-delta**2))*np.sin(wd*t))
        elif delta == 1:
            y = 1 - np.exp(-wn*t)*(1 + wn*t)
        else:
            r1 = -wn*(delta - np.sqrt(delta**2-1))
            r2 = -wn*(delta + np.sqrt(delta**2-1))
            y = 1 + (r2/(r1-r2))*np.exp(r1*t) - (r1/(r1-r2))*np.exp(r2*t)
        fig.add_trace(go.Scatter(x=t, y=y, name=name, line=dict(color=color, dash=dash, width=2.5)))

    fig.add_hline(y=1, line_dash="dot", line_color=GRAY, line_width=1, annotation_text="Final value", annotation_position="right")
    fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Output y(t)",
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(r=200),
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eeede8", zeroline=True, zerolinecolor="#ccc")
    fig.update_yaxes(showgrid=True, gridcolor="#eeede8", zeroline=True, zerolinecolor="#ccc")
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Key takeaway:** Small δ = lots of oscillation. Large δ = slow response. δ ≈ 0.3–0.7 is usually ideal in practice.")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Bode plot
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "2 · Bode plot (AR & phase)":
    st.title("Bode plot — Amplitude Ratio & Phase Angle")

    st.markdown("""
    <div class="summary-card">
    🎵 <b>Imagine shaking the system with a sine wave at different speeds.</b><br>
    The Bode plot answers: <i>"How does the output change as I shake faster and faster?"</i><br>
    It shows two things for every frequency:
    <span class="badge badge-blue">Amplitude Ratio (AR)</span> how big is the output vs input, and
    <span class="badge badge-amber">Phase angle φ</span> how far behind does the output lag.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Amplitude Ratio formula**")
        st.markdown("""<div class="formula-box">
        AR = 1 / √[(1-(ω/ωₙ)²)² + (2δ·ω/ωₙ)²]
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("**Phase angle formula**")
        st.markdown("""<div class="formula-box">
        φ = −tan⁻¹[ 2δ(ω/ωₙ) / (1−(ω/ωₙ)²) ]
        </div>""", unsafe_allow_html=True)

    # ── Controls ─────────────────────────────────────────────────────────────
    st.subheader("Interactive Bode plot")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        delta = st.slider("Damping ratio δ", 0.05, 2.0, 0.3, 0.05)
    with col_s2:
        wn_val = st.slider("Natural frequency ωₙ (rad/s)", 0.5, 10.0, 3.77, 0.1)

    wr = np.logspace(-1.5, 1.5, 400)
    AR = 1 / np.sqrt((1 - wr**2)**2 + (2*delta*wr)**2)
    phi_rad = np.arctan2(2*delta*wr, 1 - wr**2)
    phi_deg = -np.degrees(phi_rad)
    phi_deg[phi_deg > 0] -= 180

    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=["Amplitude Ratio vs ω/ωₙ", "Phase Angle vs ω/ωₙ"],
                        vertical_spacing=0.12)

    # AR
    fig.add_trace(go.Scatter(x=wr, y=AR, line=dict(color=BLUE, width=2.5), name="AR"), row=1, col=1)
    # Low-freq asymptote
    fig.add_trace(go.Scatter(x=[0.1, 1.0], y=[1, 1], line=dict(color=GRAY, dash="dash", width=1.5), name="Low-freq asymptote"), row=1, col=1)
    # High-freq asymptote
    fig.add_trace(go.Scatter(x=[1, 31], y=[1, 1/31**2], line=dict(color=GRAY, dash="dot", width=1.5), name="High-freq asymptote (slope −2)"), row=1, col=1)
    # Corner freq
    fig.add_vline(x=1.0, line_dash="longdash", line_color=CORAL, line_width=1.5, row=1, col=1)
    fig.add_annotation(x=np.log10(1.0), y=np.log10(max(AR)*0.7), text="ω = ωₙ<br>(corner)", showarrow=False, font=dict(color=CORAL, size=11), row=1, col=1)

    # Phase
    fig.add_trace(go.Scatter(x=wr, y=phi_deg, line=dict(color=AMBER, width=2.5), name="Phase φ (°)"), row=2, col=1)
    fig.add_hline(y=-90, line_dash="dash", line_color=CORAL, line_width=1, row=2, col=1, annotation_text="−90° at corner", annotation_position="right")
    fig.add_hline(y=-180, line_dash="dot", line_color=GRAY, line_width=1, row=2, col=1, annotation_text="−180° asymptote", annotation_position="right")
    fig.add_vline(x=1.0, line_dash="longdash", line_color=CORAL, line_width=1.5, row=2, col=1)

    fig.update_xaxes(type="log", title_text="ω / ωₙ  (normalized frequency)", showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(type="log", row=1, col=1, title_text="Amplitude Ratio (AR)", showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(row=2, col=1, title_text="Phase angle (°)", showgrid=True, gridcolor="#eeede8", range=[-200, 20])
    fig.update_layout(height=620, plot_bgcolor="white", paper_bgcolor="white",
                      legend=dict(orientation="h", y=-0.12))
    st.plotly_chart(fig, use_container_width=True)

    # ── Sketch guide ─────────────────────────────────────────────────────────
    st.subheader("How to sketch the Bode plot (step-by-step)")
    steps = [
        ("Step 1", "green", "Draw the LOW-FREQ asymptote: a flat horizontal line at AR = 1, from ω/ωₙ = 0.1 up to ω/ωₙ = 1."),
        ("Step 2", "green", "Draw the HIGH-FREQ asymptote: a straight line from the corner (ω/ωₙ = 1) with slope −2 on log-log axes."),
        ("Step 3", "amber", f"Add the PEAK (only if δ < 0.707): AR_peak = 1/(2δ√(1−δ²)) = {1/(2*delta*np.sqrt(max(1-delta**2, 1e-9))):.3f} at ω/ωₙ = √(1−2δ²)."),
        ("Step 4", "blue",  "For the phase plot: starts at 0°, passes through −90° at the corner, approaches −180° at high freq."),
    ]
    for label, color, text in steps:
        badge_class = f"badge-{color if color!='amber' else 'amber'}"
        st.markdown(f'<span class="badge badge-{color if color in ["blue","green"] else "amber"}">{label}</span> {text}', unsafe_allow_html=True)
        st.write("")

    st.info(f"**Current settings:** δ = {delta}, ωₙ = {wn_val} rad/s → Corner at ω = {wn_val:.2f} rad/s")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Peak AR & corner frequency
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "3 · Peak AR & corner frequency":
    st.title("Peak Amplitude Ratio & Corner Frequency")

    st.markdown("""
    <div class="summary-card">
    🔔 <b>Resonance:</b> When δ is small, there's a frequency where the system resonates —
    like pushing a swing at just the right moment. At that frequency, the output is
    <i>larger</i> than the input. This is dangerous in engineering systems!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Peak frequency")
        st.markdown("""<div class="formula-box">ω_peak / ωₙ = √(1 − 2δ²)</div>""", unsafe_allow_html=True)
        st.write("Only exists when **δ < 1/√2 ≈ 0.707**. As δ → 0, ω_peak → ωₙ.")
    with col2:
        st.subheader("Peak amplitude ratio")
        st.markdown("""<div class="formula-box">AR_peak = 1 / (2δ√(1 − δ²))</div>""", unsafe_allow_html=True)
        st.write("As δ → 0, AR_peak → ∞. When δ = 0.707, the peak disappears (AR_peak = 1).")

    st.subheader("Explore how δ affects the peak")
    delta = st.slider("Damping ratio δ", 0.05, 1.4, 0.3, 0.05, key="peak_slider")

    wr = np.logspace(-1.5, 1.5, 500)
    AR = 1 / np.sqrt((1 - wr**2)**2 + (2*delta*wr)**2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wr, y=AR, line=dict(color=BLUE, width=3), name=f"AR (δ={delta})"))

    if delta < 1/np.sqrt(2):
        wr_peak = np.sqrt(1 - 2*delta**2)
        ar_peak = 1 / (2*delta*np.sqrt(1 - delta**2))
        fig.add_trace(go.Scatter(
            x=[wr_peak], y=[ar_peak],
            mode="markers+text",
            marker=dict(color=CORAL, size=12, symbol="star"),
            text=[f"  AR_peak = {ar_peak:.3f}<br>  ω/ωₙ = {wr_peak:.3f}"],
            textposition="middle right",
            name="Peak",
            textfont=dict(color=CORAL, size=12),
        ))
        fig.add_vline(x=wr_peak, line_dash="dash", line_color=CORAL, line_width=1)

    fig.add_vline(x=1.0, line_dash="longdash", line_color=GRAY, line_width=1.5, annotation_text="Corner (ωₙ)", annotation_position="top right")
    fig.add_hline(y=1.0, line_dash="dot", line_color=GRAY, line_width=1)

    fig.update_xaxes(type="log", title="ω / ωₙ", showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(type="log", title="Amplitude Ratio", showgrid=True, gridcolor="#eeede8")
    fig.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    # ── Summary numbers ──────────────────────────────────────────────────────
    st.subheader("Computed values")
    c1, c2, c3 = st.columns(3)
    if delta < 1/np.sqrt(2):
        wr_peak = np.sqrt(1 - 2*delta**2)
        ar_peak = 1 / (2*delta*np.sqrt(1 - delta**2))
        c1.metric("Peak AR", f"{ar_peak:.4f}")
        c2.metric("ω_peak / ωₙ", f"{wr_peak:.4f}")
        c3.metric("Phase at corner", "−90°")
    else:
        c1.metric("Peak AR", "No peak (δ ≥ 0.707)")
        c2.metric("ω_peak / ωₙ", "N/A")
        c3.metric("Phase at corner", "−90°")

    st.markdown("---")
    st.subheader("Corner frequency — the key rule")
    st.markdown("""
    <div class="formula-box">
    Corner frequency = ωₙ<br><br>
    At ω = ωₙ  →  phase angle = −90°  (always, for any δ)<br>
    At ω = ωₙ  →  the two asymptotes intersect on the Bode plot
    </div>
    """, unsafe_allow_html=True)
    st.info("🔑 The corner frequency is always ωₙ. You find it from the system equations. The phase is always −90° there.")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Steady-state gain & potential value
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "4 · Steady-state gain & potential value":
    st.title("Steady-state gain & potential value")

    st.markdown("""
    <div class="summary-card">
    ⚖️ <b>Steady-state gain K</b> is the ratio of output to input once everything has settled.
    If you double the input and K = 3, the output triples. If K = 1, output equals input.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1st-order with gain")
        st.markdown("""<div class="formula-box">G(s) = K / (1 + T·s)</div>""", unsafe_allow_html=True)
        st.write("At steady state, s → 0, so G → K.")
    with col2:
        st.subheader("2nd-order with gain")
        st.markdown("""<div class="formula-box">G(s) = K / (1 + 2δ/ωₙ·s + s²/ωₙ²)</div>""", unsafe_allow_html=True)
        st.write("At steady state, s → 0, so G → K again.")

    st.subheader("Effect of K on step response")
    col_s1, col_s2, col_s3 = st.columns(3)
    K     = col_s1.slider("Static gain K", 0.2, 3.0, 1.0, 0.1)
    delta = col_s2.slider("Damping ratio δ", 0.1, 2.0, 0.5, 0.05, key="gain_d")
    wn_g  = col_s3.slider("ωₙ (rad/s)", 0.5, 5.0, 2.0, 0.1, key="gain_wn")

    t = np.linspace(0, 12, 500)
    wd = wn_g * np.sqrt(abs(1 - delta**2))
    if delta < 1:
        y = K * (1 - np.exp(-delta*wn_g*t)*(np.cos(wd*t) + (delta/np.sqrt(1-delta**2))*np.sin(wd*t)))
    elif delta == 1:
        y = K * (1 - np.exp(-wn_g*t)*(1 + wn_g*t))
    else:
        r1 = -wn_g*(delta - np.sqrt(delta**2-1))
        r2 = -wn_g*(delta + np.sqrt(delta**2-1))
        y = K * (1 + (r2/(r1-r2))*np.exp(r1*t) - (r1/(r1-r2))*np.exp(r2*t))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, line=dict(color=BLUE, width=2.5), name="System output"))
    fig.add_hline(y=K, line_dash="dash", line_color=CORAL, line_width=1.5, annotation_text=f"Steady-state = K = {K}", annotation_position="right")
    fig.add_hline(y=1, line_dash="dot", line_color=GRAY, line_width=1, annotation_text="Input = 1", annotation_position="right")
    fig.update_layout(height=360, plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="Time (s)", yaxis_title="Output")
    fig.update_xaxes(showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(showgrid=True, gridcolor="#eeede8")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Steady-state output = {K:.2f}** (= K × input of 1)")

    st.markdown("---")
    st.subheader("Potential value — the useful trick")
    st.markdown("""
    When K ≠ 1, split the system into two blocks:
    - **Block 1:** just the static gain K → turns input Xᵢ into "potential value" Yᵢ
    - **Block 2:** standard unit-gain transfer function 1/(1+Ts)

    This lets you use the standard dimensionless Bode charts directly.
    """)
    st.markdown("""<div class="formula-box">
    Xᵢ → [K] → Yᵢ (potential value) → [1/(1+Ts)] → Y
    </div>""", unsafe_allow_html=True)
    st.info("💡 Yᵢ is the steady-state output that would correspond to input Xᵢ — it 'converts' the units so you can use standard charts.")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Linearization
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "5 · Linearization":
    st.title("Linearization")

    st.markdown("""
    <div class="summary-card">
    📐 <b>The big idea:</b> Most real systems are nonlinear (curved). But our tools — Laplace,
    transfer functions, Bode plots — only work for <i>linear</i> equations. Linearization lets
    us approximate a curved equation with a straight line near one operating point.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("The core idea — zoom in close enough, any curve looks straight")

    col_s1, col_s2 = st.columns(2)
    h0     = col_s1.slider("Operating point h₀", 0.5, 4.0, 2.0, 0.1)
    zoom   = col_s2.slider("Zoom level (range around h₀)", 0.2, 3.0, 2.0, 0.1)

    h = np.linspace(0, 5, 400)
    Q_curve = np.sqrt(np.maximum(h, 0))
    dQ_dh   = 1 / (2 * np.sqrt(h0))
    h_zoom  = np.linspace(h0 - zoom, h0 + zoom, 100)
    Q_linear = np.sqrt(h0) + dQ_dh * (h_zoom - h0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h, y=Q_curve, line=dict(color=BLUE, width=2.5), name="Q = √h  (nonlinear)"))
    fig.add_trace(go.Scatter(x=h_zoom, y=Q_linear, line=dict(color=CORAL, width=2.5, dash="dash"), name=f"Tangent at h₀={h0} (linear approx)"))
    fig.add_trace(go.Scatter(x=[h0], y=[np.sqrt(h0)], mode="markers", marker=dict(color=AMBER, size=12, symbol="circle"), name="Operating point"))
    fig.update_layout(height=360, plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="h", yaxis_title="Q")
    fig.update_xaxes(showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(showgrid=True, gridcolor="#eeede8")
    st.plotly_chart(fig, use_container_width=True)

    dQ = dQ_dh
    st.markdown(f"""
    <div class="formula-box">
    At h₀ = {h0}:  dQ/dh|₀ = 1/(2√{h0}) = {dQ:.4f}<br><br>
    Linearized:  Q̂ = {dQ:.4f} · ĥ     (where ĥ = h − {h0})
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Types of nonlinearities in chemical processes")

    nl_types = {
        "Curvature (e.g. Q ∝ √h)": ("Can linearize near operating point. Most common in ChE.", TEAL),
        "Saturation": ("Linear region up to a limit, then flat. Linearize only in rising zone.", AMBER),
        "Dead zone": ("No response until threshold crossed. Tricky to linearize.", CORAL),
        "Hysteresis": ("Different path going up vs going down. Cannot be linearized simply.", PURPLE),
    }

    for name, (desc, color) in nl_types.items():
        st.markdown(f"**{name}** — {desc}")

    st.markdown("---")
    st.subheader("Linearizing a product term — z = q·y")
    st.markdown("""
    Products of two variables are nonlinear. We use the partial derivative rule:
    """)
    st.markdown("""<div class="formula-box">
    z = q · y<br><br>
    ẑ = (∂z/∂q)|₀ · q̂  +  (∂z/∂y)|₀ · ŷ<br><br>
    ẑ = y₀ · q̂  +  q₀ · ŷ
    </div>""", unsafe_allow_html=True)
    st.info("🔑 Hat variables (like q̂, ŷ) mean the *deviation* from steady state, not the actual value. At steady state, all hat variables = 0.")

    st.subheader("When is linearization valid?")
    st.markdown("""
    - ✅ When deviations from steady state are **small** (which they are under automatic control)
    - ✅ For **curvature** type nonlinearities
    - ❌ For **large excursions** (e.g. start-up problems)
    - ❌ For **sharp discontinuities** (saturation limits, dead zones)
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Worked Example: Manometer
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "6 · Worked example — Manometer":
    st.title("Worked example — Mercury manometer (Sheet 2, Problem 7)")

    st.markdown("""
    <div class="summary-card">
    A mercury manometer has mercury length L = 54.25 in, tube diameter D = 0.05 in,
    and mercury viscosity μ = 1.6 cP. A sinusoidal pressure input is applied.
    Find all frequency response characteristics.
    </div>
    """, unsafe_allow_html=True)

    # ── Given data ───────────────────────────────────────────────────────────
    st.subheader("Given data & system parameters")
    L_in  = 54.25
    D_in  = 0.05
    mu_cp = 1.6
    rho   = 13600   # kg/m³ mercury
    g     = 9.81

    L = L_in * 0.0254
    D = D_in * 0.0254
    mu = mu_cp * 1e-3

    wn = np.sqrt(2*g/L)
    delta = (8*mu*L) / (rho*g*D**2 * np.sqrt(L/(2*g)))
    # Corrected formula from lecture: 2δ/ωₙ = 16Lμ/(ρgD²) → δ = 8Lμωₙ/(ρgD²)
    delta = (8 * mu / (rho * g * D**2)) * np.sqrt(2*g*L)

    col1, col2, col3 = st.columns(3)
    col1.metric("ωₙ (rad/s)", f"{wn:.4f}")
    col2.metric("δ (damping ratio)", f"{delta:.4f}")
    col3.metric("δ < 0.707?", "Yes — peak exists" if delta < 1/np.sqrt(2) else "No peak")

    st.markdown("""<div class="formula-box">
    ωₙ = √(2g/L)   and   δ = (8μ/ρgD²)·√(2gL)
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Part A ───────────────────────────────────────────────────────────────
    st.subheader("Part A — Highest amplitude ratio")
    if delta < 1/np.sqrt(2):
        ar_peak = 1 / (2*delta*np.sqrt(1-delta**2))
        st.markdown(f"""<div class="formula-box">
        AR_peak = 1/(2δ√(1−δ²)) = 1/(2×{delta:.4f}×√(1−{delta**2:.4f})) = <b>{ar_peak:.4f}</b>
        </div>""", unsafe_allow_html=True)
    st.success(f"✅ Maximum AR = **{ar_peak:.4f}**")

    # ── Part B ───────────────────────────────────────────────────────────────
    st.subheader("Part B — Frequency of peak AR")
    wr_peak = np.sqrt(1 - 2*delta**2)
    w_peak  = wr_peak * wn
    f_peak  = w_peak / (2*np.pi)
    st.markdown(f"""<div class="formula-box">
    ω/ωₙ|_peak = √(1−2δ²) = {wr_peak:.4f}<br>
    ω_peak = {wr_peak:.4f} × {wn:.4f} = {w_peak:.4f} rad/s<br>
    f_peak = {w_peak:.4f}/(2π) = {f_peak:.4f} cycles/s
    </div>""", unsafe_allow_html=True)
    st.success(f"✅ Peak at ω = **{w_peak:.3f} rad/s** = **{f_peak:.4f} Hz**")

    # ── Part C ───────────────────────────────────────────────────────────────
    st.subheader("Part C — AR at 3 cycles/s")
    f_c  = 3.0
    w_c  = 2*np.pi*f_c
    wr_c = w_c / wn
    AR_c = 1 / np.sqrt((1-wr_c**2)**2 + (2*delta*wr_c)**2)
    st.markdown(f"""<div class="formula-box">
    ω = 2π×3 = {w_c:.3f} rad/s   →   ω/ωₙ = {wr_c:.3f}<br>
    AR = 1/√[(1−{wr_c**2:.3f})² + (2×{delta:.4f}×{wr_c:.3f})²] = {AR_c:.4f}
    </div>""", unsafe_allow_html=True)
    st.success(f"✅ AR at 3 Hz = **{AR_c:.4f}**")

    # ── Part D ───────────────────────────────────────────────────────────────
    st.subheader("Part D — Frequency where AR < 0.05")
    wr_vals = np.linspace(1, 20, 5000)
    AR_vals = 1 / np.sqrt((1-wr_vals**2)**2 + (2*delta*wr_vals)**2)
    idx = np.where(AR_vals < 0.05)[0]
    if len(idx):
        wr_lim = wr_vals[idx[0]]
        w_lim  = wr_lim * wn
        f_lim  = w_lim / (2*np.pi)
        st.markdown(f"""<div class="formula-box">
        AR &lt; 0.05 when ω/ωₙ ≈ {wr_lim:.2f}  →  ω = {w_lim:.2f} rad/s  →  f = {f_lim:.2f} Hz
        </div>""", unsafe_allow_html=True)
        st.success(f"✅ AR < 0.05 when f > **{f_lim:.2f} cycles/s**")

    # ── Full Bode plot for manometer ─────────────────────────────────────────
    st.subheader("Full Bode plot for this manometer")
    wr_full = np.logspace(-1.5, 1.5, 600)
    AR_full = 1 / np.sqrt((1-wr_full**2)**2 + (2*delta*wr_full)**2)
    phi_full = np.degrees(-np.arctan2(2*delta*wr_full, 1-wr_full**2))
    phi_full[phi_full > 0] -= 180

    fig = make_subplots(rows=2, cols=1, subplot_titles=["Amplitude Ratio", "Phase Angle"],
                        vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=wr_full, y=AR_full, line=dict(color=BLUE, width=2.5), name="AR"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[wr_peak], y=[ar_peak], mode="markers+text",
                             marker=dict(color=CORAL, size=12, symbol="star"),
                             text=[f" Peak={ar_peak:.3f}"], textposition="middle right",
                             textfont=dict(color=CORAL), name="Peak AR"), row=1, col=1)
    fig.add_hline(y=0.05, line_dash="dash", line_color=AMBER, line_width=1.5,
                  annotation_text="AR = 0.05", annotation_position="right", row=1, col=1)

    fig.add_trace(go.Scatter(x=wr_full, y=phi_full, line=dict(color=AMBER, width=2.5), name="Phase"), row=2, col=1)
    fig.add_hline(y=-90, line_dash="dash", line_color=GRAY, line_width=1, row=2, col=1,
                  annotation_text="−90°", annotation_position="right")

    fig.update_xaxes(type="log", title_text="ω / ωₙ", showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(type="log", row=1, col=1, title_text="AR", showgrid=True, gridcolor="#eeede8")
    fig.update_yaxes(row=2, col=1, title_text="Phase (°)", showgrid=True, gridcolor="#eeede8", range=[-200, 10])
    fig.update_layout(height=560, plot_bgcolor="white", paper_bgcolor="white",
                      legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"**Summary:** ωₙ = {wn:.4f} rad/s, δ = {delta:.4f}, AR_peak = {ar_peak:.4f} at f = {f_peak:.4f} Hz")
