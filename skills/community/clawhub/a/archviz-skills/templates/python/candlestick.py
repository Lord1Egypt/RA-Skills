"""archviz-skills — Candlestick (Plotly, restrained)"""
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(
    x=["Mon","Tue","Wed","Thu","Fri"],
    open=[100,102,101,105,103],
    high=[105,106,107,108,110],
    low=[98,100,99,102,101],
    close=[102,101,105,103,108],
    increasing_line_color="#002FA7",
    decreasing_line_color="#94a3b8",
    increasing_fillcolor="rgba(0,47,167,0.3)",
    decreasing_fillcolor="rgba(148,163,184,0.3)"
)])
fig.update_layout(
    title="Price Movement",
    paper_bgcolor="#f5f0eb", plot_bgcolor="#f5f0eb",
    font=dict(family="system-ui", color="#44403c", size=13),
    xaxis=dict(gridcolor="#d6d3d1"),
    yaxis=dict(title="Price", gridcolor="#d6d3d1"),
    xaxis_rangeslider_visible=False
)
fig.write_html("candlestick.html")
print("Saved: candlestick.html")
