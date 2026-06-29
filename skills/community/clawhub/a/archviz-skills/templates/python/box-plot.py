"""archviz-skills — Box Plot + Violin (Plotly, restrained)"""
import plotly.graph_objects as go
import numpy as np

np.random.seed(42)
groups = ["Group A", "Group B", "Group C", "Group D"]
data = [np.random.normal(loc=m, scale=s, size=100) for m, s in zip([50, 60, 45, 70], [10, 15, 8, 12])]

fig = go.Figure()
for i, (g, d) in enumerate(zip(groups, data)):
    fig.add_trace(go.Box(y=d, name=g, marker_color=["#002FA7","#94a3b8","#a8a29e","#d6d3d1"][i],
                         boxmean="sd", line_width=1.5))

fig.update_layout(
    title="Distribution by Group",
    paper_bgcolor="#f5f0eb", plot_bgcolor="#f5f0eb",
    font=dict(family="system-ui", color="#44403c", size=13),
    yaxis=dict(title="Value", gridcolor="#d6d3d1"),
    showlegend=False
)
fig.write_html("box-plot.html")
print("Saved: box-plot.html")
