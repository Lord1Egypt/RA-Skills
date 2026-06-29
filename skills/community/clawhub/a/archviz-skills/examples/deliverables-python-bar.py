# Deliverables Python bar (from archviz-skills; env=deliverables, type=ranking per report).
# Use Plotly for interactive HTML export (or Matplotlib for static).
# Agent vibes this from brief; user runs for 落作品.
# Restrained: warm paper bg, IKB accent, short labels/codes.

import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'Phase': ['V1.1 Env Setup', 'V1.2 Ledger', 'V1.3 Settle'],  # Codes + full in table if needed
    'Weeks': [6, 7, 4]
})

fig = px.bar(df, x='Phase', y='Weeks', title='Project Phases (V1) - restrained',
             color_discrete_sequence=['#002FA7'])  # IKB

fig.update_layout(
    plot_bgcolor='#f5f0eb',  # Warm paper
    paper_bgcolor='#f5f0eb',
    font_color='#1B365D',
    xaxis_title=None,
    yaxis_title='Weeks',
    showlegend=False
)

fig.write_html('project-phases-v1.html')  # Interactive HTML for deliverable
print('Generated: project-phases-v1.html (open for final work)')

# For static/PDF: uncomment Matplotlib
# import matplotlib.pyplot as plt
# plt.style.use('seaborn-v0_8-whitegrid')  # Minimal
# ... plot, savefig('project-phases-v1.png', facecolor='#f5f0eb', dpi=300)
```

**Notes (per skill):**
- Env=deliverables → full Python.
- Type from report: ranking → bar.
- For Gantt etc.: adapt to px.timeline.
- Icons: add as annotations if needed.
- Author habit: direct.
- Later run this for 落作品; OB version above for preview.