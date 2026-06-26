---
name: data-report-generator
description: |
  Automatically analyze CSV or Excel files and generate professional data analysis reports with charts, 
  summaries, and insights — output as Word (.docx) or PDF. Use this skill whenever the user uploads or 
  mentions a data file (CSV, Excel, .xlsx, .xls) and wants a report, analysis, summary, dashboard, or 
  visualization of that data. Also trigger when users say things like "analyze my data", "make a report 
  from this spreadsheet", "visualize this CSV", "generate charts from my sales data", "weekly/monthly 
  report", "data summary", "turn this into a report", or ask for any kind of automated reporting from 
  tabular data. Ideal for operations, sales, marketing, and finance teams.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
        - pip
---

# Data Report Generator

Transform raw CSV or Excel files into professional, insight-rich reports with charts — output as Word (.docx) or PDF.

## When This Skill Activates

Trigger when user provides:
- A CSV, Excel (.xlsx/.xls), or TSV file + asks for a report/analysis
- A request to "visualize", "summarize", or "analyze" tabular data
- Any mention of automated weekly/monthly reporting

If no file is uploaded yet, ask the user to upload their data file first.

---

## Step 1: Gather Inputs

Ask for (or infer from context):
1. **Data file** — CSV, Excel, TSV (required)
2. **Report format** — Word (.docx) or PDF? (default: Word)
3. **Report purpose** — sales analysis? operations? marketing? financial? (affects framing)
4. **Key questions** — what does the user most want to understand from this data?
5. **Audience** — internal team? executive summary? client-facing?
6. **Language** — Chinese or English? (default: match user's language)

If purpose/questions aren't specified, proceed with a comprehensive general analysis.

---

## Step 2: Read and Profile the Data

```python
import pandas as pd
import numpy as np

# Support both CSV and Excel
def load_data(filepath):
    ext = filepath.rsplit('.', 1)[-1].lower()
    if ext in ['xlsx', 'xls']:
        df = pd.read_excel(filepath)
    elif ext == 'csv':
        # Try common encodings
        for enc in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
            try:
                df = pd.read_csv(filepath, encoding=enc)
                break
            except:
                continue
    elif ext == 'tsv':
        df = pd.read_csv(filepath, sep='\t')
    return df

df = load_data('/path/to/file')
```

### Data Profile to Extract

- Shape: row count, column count
- Column types: numeric, categorical, date/time, text
- Missing values: count and % per column
- Basic stats: mean, median, min, max, std for numeric columns
- Unique value counts for categorical columns
- Date range if time columns exist
- Obvious data quality issues

---

## Step 3: Auto-Detect Report Type

Based on column names and data types, auto-select the analysis approach:

| Data Pattern | Report Type | Reference File |
|---|---|---|
| Date column + numeric values | **Time Series / Trend** | `references/time-series.md` |
| Category + numeric (sales/revenue) | **Sales / Performance** | `references/sales-analysis.md` |
| Multiple numeric columns | **Correlation / Distribution** | `references/statistical.md` |
| Category breakdowns only | **Segmentation** | `references/segmentation.md` |
| Mixed / unknown | **General Analysis** | `references/general.md` |

Read the relevant reference file for chart selection and narrative guidance.

If the user specifies a report type, use that. Otherwise, auto-detect.

---

## Step 4: Generate Charts

Install dependencies first:

```bash
pip install matplotlib seaborn pandas openpyxl --break-system-packages --quiet
```

### Chart Generation Rules

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — ALWAYS set this
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Style setup — professional look
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']

def save_chart(fig, filename):
    fig.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
```

### Chart Selection Guide

**Time series data** → Line chart (trend) + bar chart (period comparison)
```python
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['date'], df['value'], color=COLORS[0], linewidth=2, marker='o', markersize=4)
ax.set_title('Trend Over Time', fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
save_chart(fig, 'chart_trend.png')
```

**Category comparison** → Horizontal bar chart (easier to read labels)
```python
fig, ax = plt.subplots(figsize=(10, 6))
df_sorted = df.sort_values('value', ascending=True)
bars = ax.barh(df_sorted['category'], df_sorted['value'], color=COLORS[0])
ax.bar_label(bars, fmt='%.1f', padding=3)
ax.set_title('Performance by Category', fontsize=14, fontweight='bold')
save_chart(fig, 'chart_category.png')
```

**Distribution** → Histogram + optional KDE
```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['value'].dropna(), bins=30, color=COLORS[0], edgecolor='white', alpha=0.8)
ax.set_title('Value Distribution', fontsize=14, fontweight='bold')
save_chart(fig, 'chart_dist.png')
```

**Composition/share** → Pie or stacked bar (prefer stacked bar for >5 categories)
```python
fig, ax = plt.subplots(figsize=(8, 6))
sizes = df['value']
labels = df['category']
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                   colors=COLORS, startangle=90)
ax.set_title('Composition', fontsize=14, fontweight='bold')
save_chart(fig, 'chart_pie.png')
```

**Correlation** → Heatmap
```python
fig, ax = plt.subplots(figsize=(10, 8))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            ax=ax, square=True, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
save_chart(fig, 'chart_corr.png')
```

**Generate 3–6 charts total** — enough to be comprehensive, not overwhelming.

---

## Step 5: Write the Report (Word .docx)

Use the `docx` Python library. Install: `pip install python-docx --break-system-packages --quiet`

### Report Structure

```
1. Cover Page
   - Report title, data source name, date generated
2. Executive Summary (1 page)
   - 3-5 key findings in plain language
   - Most important metric highlighted
3. Data Overview
   - Dataset dimensions, time range, data quality notes
4. [Core Analysis Sections — vary by report type]
   - Each section: narrative paragraph + chart + key takeaways
5. Key Insights & Recommendations
   - Actionable bullet points
6. Appendix: Data Statistics Table
```

### Docx Code Pattern

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import datetime

doc = Document()

# Page setup
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.left_margin = Inches(1)
section.right_margin = Inches(1)
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)

# Title style
def add_title(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = heading.runs[0]
    run.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)  # Brand blue
    return heading

# Body text
def add_paragraph(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    run = p.runs[0] if p.runs else p.add_run()
    run.font.size = Pt(11)
    return p

# Insert chart image
def add_chart(doc, image_path, caption, width=6.0):
    doc.add_picture(image_path, width=Inches(width))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# Stats table
def add_stats_table(doc, df):
    stats = df.describe().round(2)
    table = doc.add_table(rows=len(stats)+1, cols=len(stats.columns)+1)
    table.style = 'Table Grid'
    # Header row
    table.cell(0, 0).text = 'Metric'
    for j, col in enumerate(stats.columns):
        table.cell(0, j+1).text = str(col)
    # Data rows
    for i, idx in enumerate(stats.index):
        table.cell(i+1, 0).text = str(idx)
        for j, col in enumerate(stats.columns):
            table.cell(i+1, j+1).text = str(stats.loc[idx, col])

# Save
doc.save('/home/claude/report_output.docx')
```

---

## Step 6: Convert to PDF (if requested)

```bash
# Use LibreOffice for conversion
python /path/to/skills/docx/scripts/office/soffice.py \
  --headless --convert-to pdf /home/claude/report_output.docx \
  --outdir /home/claude/
```

If LibreOffice is unavailable, fall back to `reportlab`:
```bash
pip install reportlab --break-system-packages --quiet
```
See `references/pdf-fallback.md` for reportlab-based PDF generation.

---

## Step 7: Output to User

1. Copy final file to `/mnt/user-data/outputs/`
2. Use `present_files` tool to share it
3. Include a brief summary in chat:
   - What data was analyzed
   - How many charts were generated
   - Top 3 insights found
   - Any data quality issues to be aware of

---

## Output Quality Checklist

Before delivering, verify:
- [ ] Charts have titles, axis labels, and readable fonts
- [ ] No blank/empty chart images
- [ ] Report has executive summary with plain-language findings
- [ ] Data quality issues are noted (missing values, anomalies)
- [ ] File opens cleanly (test docx structure validity)
- [ ] Chinese text renders correctly if using Chinese (use `SimHei` or `Microsoft YaHei` font in matplotlib)
- [ ] All chart image files exist before embedding in docx

---

## Handling Chinese / CJK Text in Charts

```python
import matplotlib
# Set Chinese-compatible font
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 
                                           'PingFang SC', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False  # Fix minus sign rendering
```

If font not available on system:
```bash
pip install matplotlib --break-system-packages
# Download and install a CJK font
apt-get install -y fonts-wqy-zenhei 2>/dev/null || true
```

---

## Edge Cases

**Large datasets (>100k rows)**: Sample or aggregate before visualization. Note sampling in report.

**Messy/dirty data**: Document cleaning steps in the report's "Data Overview" section. Show before/after counts.

**Single column data**: Generate distribution analysis only. Note limitation.

**All categorical data**: Focus on frequency analysis and cross-tabulations. No numeric charts.

**Date parsing issues**: Try multiple date formats (`dayfirst=True`, `yearfirst=True`, `infer_datetime_format=True`).

**Multiple sheets in Excel**: Ask user which sheet(s) to analyze, or analyze all and create multi-section report.

---

## Reference Files

- `references/time-series.md` — Trend analysis, seasonality detection, period-over-period comparisons
- `references/sales-analysis.md` — Sales/revenue specific charts, KPI calculations, funnel analysis
- `references/statistical.md` — Correlation, distribution, outlier detection, regression
- `references/segmentation.md` — Category breakdowns, cohort analysis, ranking
- `references/general.md` — General-purpose analysis for unknown data types
- `references/pdf-fallback.md` — PDF generation with reportlab when LibreOffice unavailable
- `references/chart-styling.md` — Advanced chart styling, brand colors, annotation patterns
