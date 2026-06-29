"""archviz-skills — Parallel Coordinates (Plotly, restrained)"""
import plotly.graph_objects as go

fig = go.Figure(data=go.Parcoords(
    line=dict(color=["#002FA7","#94a3b8","#a8a29e","#d6d3d1","#7a8fa0"]),
    dimensions=[
        dict(label="Speed", values=[80, 60, 90, 45, 70], range=[0,100]),
        dict(label="Quality", values=[70, 85, 65, 90, 75], range=[0,100]),
        dict(label="Cost", values=[30, 70, 50, 85, 60], range=[0,100]),
        dict(label="Scale", values=[90, 55, 80, 40, 85], range=[0,100]),
    ]
))
fig.update_layout(
    title="Multi-dimensional Comparison",
    paper_bgcolor="#f5f0eb", font=dict(family="system-ui", color="#44403c", size=13)
)
fig.write_html("parallel-coords.html")
print("Saved: parallel-coords.html")
