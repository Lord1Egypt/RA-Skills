# Chart Styling Reference

## Brand Color Palettes

```python
# Default professional palette
COLORS_DEFAULT = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#44BBA4', '#3B1F2B', '#E9C46A']

# Blue-focused (tech/SaaS)
COLORS_TECH = ['#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8', '#023E8A']

# Warm (retail/consumer)
COLORS_WARM = ['#E63946', '#F4A261', '#E9C46A', '#2A9D8F', '#264653']

# Green-positive (growth/finance)
COLORS_FINANCE = ['#2DC653', '#4CAF50', '#FFC107', '#FF5722', '#9C27B0']

# Red/green for gains/losses
COLOR_POSITIVE = '#44BBA4'
COLOR_NEGATIVE = '#C73E1D'
COLOR_NEUTRAL  = '#888888'
```

## Global Style Setup

```python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.use('Agg')  # MUST be called before any other matplotlib imports

# Global style
plt.style.use('seaborn-v0_8-whitegrid')
matplotlib.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 10,
    'figure.dpi': 100,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white',
    # CJK font support
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'DejaVu Sans', 'Arial'],
    'axes.unicode_minus': False,
})
```

## Number Formatting

```python
# Format large numbers with K/M suffix
def format_number(n):
    if abs(n) >= 1_000_000:
        return f'{n/1_000_000:.1f}M'
    elif abs(n) >= 1_000:
        return f'{n/1_000:.1f}K'
    return f'{n:.0f}'

# Apply to axis
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format_number(x)))

# Percentage axis
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
```

## Chart Annotations

```python
# Annotate max/min points on line chart
max_idx = df['value'].idxmax()
min_idx = df['value'].idxmin()

ax.annotate(f"Max: {df.loc[max_idx, 'value']:.0f}",
    xy=(df.loc[max_idx, 'date'], df.loc[max_idx, 'value']),
    xytext=(10, 10), textcoords='offset points',
    fontsize=9, color='#2E86AB',
    arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=1.5))

# Add trend line
import numpy as np
z = np.polyfit(range(len(df)), df['value'], 1)
p = np.poly1d(z)
ax.plot(df['date'], p(range(len(df))), '--', color='#F18F01', linewidth=1.5,
        label='Trend', alpha=0.7)
```

## Multi-Chart Dashboard Layout

```python
# 2x2 grid dashboard
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Data Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)

ax1 = fig.add_subplot(2, 2, 1)  # Top-left: Trend
ax2 = fig.add_subplot(2, 2, 2)  # Top-right: Category bar
ax3 = fig.add_subplot(2, 2, 3)  # Bottom-left: Composition
ax4 = fig.add_subplot(2, 2, 4)  # Bottom-right: Distribution

# ... plot to each ax ...

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig('dashboard.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

## Table Formatting in Reports

```python
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def style_table(table):
    """Apply professional styling to a docx table"""
    # Header row — dark background
    header_row = table.rows[0]
    for cell in header_row.cells:
        cell._tc.get_or_add_tcPr()
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), '2E86AB')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:val'), 'clear')
        cell._tc.tcPr.append(shading)
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.bold = True
                run.font.size = Pt(10)
    
    # Data rows — alternating shading
    for i, row in enumerate(table.rows[1:]):
        fill = 'F0F7FB' if i % 2 == 0 else 'FFFFFF'
        for cell in row.cells:
            cell._tc.get_or_add_tcPr()
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), fill)
            shading.set(qn('w:val'), 'clear')
            cell._tc.tcPr.append(shading)
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9)
```

## Save Chart Helper

```python
def save_chart(fig, filename, title=None):
    """Standardized chart saving"""
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold')
    fig.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"✓ Saved: {filename}")
    return filename
```
