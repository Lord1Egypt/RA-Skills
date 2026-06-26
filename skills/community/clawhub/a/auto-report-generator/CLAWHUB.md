# ClawHub Listing — Auto Report Generator

## Basic Info

| Field | Value |
|-------|-------|
| **Slug** | `auto-report-generator` |
| **Name** | Auto Report Generator |
| **Category** | Productivity / Data & Analytics |
| **Tags** | `report`, `analytics`, `chart`, `data`, `CSV`, `Excel`, `automation`, `monthly-report` |

---

## Description (English)

Upload CSV or Excel data and let AI automatically generate professional reports with charts and textual analysis. Perfect for monthly reports, financial summaries, and sales analytics.

**What it does:**
- Imports data from CSV/Excel files
- AI analyzes patterns, trends, and anomalies
- Generates professional charts (line, bar, pie, scatter, area, heatmap)
- Produces formatted Excel reports with multiple sheets
- Provides AI-written data insights and summaries

---

## Features

- **Data Import**: CSV and Excel (.xlsx/.xls) file support
- **AI Analysis**: Automatic pattern detection and trend analysis using OpenAI-compatible APIs
- **Chart Generation**: 6 chart types — line, bar, pie, scatter, area, heatmap
- **Multi-sheet Excel Export**: Professional formatting with title, data, and charts sheets
- **Report Templates**: Monthly, Financial, Sales, Comparison, Custom
- **Quota Management**: Built-in tier system with usage tracking
- **CLI Interface**: Easy command-line usage with shell script support
- **Python API**: Programmatic access for integration into other tools

---

## Requirements

```
pandas>=1.3.0
openpyxl>=3.0.0
xlsxwriter>=3.0.0
matplotlib>=3.4.0
Pillow>=8.0.0
requests>=2.25.0
numpy>=1.20.0
```

**Runtime Requirements:**
- Python 3.8+
- OpenAI API key (or DeepSeek API key) for AI features

---

## Pricing

| Tier | Price | Monthly Quota | Charts | PDF Export |
|------|-------|--------------|--------|------------|
| **FREE** | ¥0 | 5 (lifetime) | 1/report | No |
| **STD** | ¥9.9/mo | 50 | 3/report | No |
| **PRO** | ¥29.9/mo | 200 | Unlimited | Yes |
| **MAX** | ¥99/mo | Unlimited | Unlimited | Yes + Custom Templates |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export OPENAI_API_KEY="sk-your-key-here"

# 3. Generate a report
python scripts/generator.py \
    --file your_data.csv \
    --template monthly \
    --output report.xlsx

# Or use the shell script
chmod +x scripts/quick_report.sh
./scripts/quick_report.sh sales_data.xlsx monthly
```

---

## File Structure

```
auto-report-generator/
├── SKILL.md          # Skill definition
├── README.md          # Documentation
├── requirements.txt   # Python dependencies
├── CLAWHUB.md         # ClawHub listing (this file)
├── SKILLHUB.md        # Volcengine Skillhub listing
├── scripts/
│   ├── generator.py   # Main CLI generator
│   └── quick_report.sh # Quick report shell script
└── core/
    ├── parser.py       # Data parser (pandas)
    ├── charts.py       # Chart generation (matplotlib)
    ├── ai_analyzer.py  # AI analysis (OpenAI)
    ├── report_builder.py # Excel report builder
    ├── quota.py        # Quota management
    └── templates.py    # Template system
```

---

## Use Cases

- **Monthly Reports**: Automate repetitive monthly business reports
- **Financial Analysis**: Generate P&L statements and financial summaries
- **Sales Analytics**: Track sales performance with visual charts
- **Data Comparison**: Side-by-side comparison of metrics across periods
- **Custom Reports**: Build custom report templates for specific needs

---

## Notes

- Free tier is limited to 5 total uses (lifetime), not per month
- Charts are generated using matplotlib and embedded in Excel files
- AI analysis requires a valid API key for OpenAI or DeepSeek
- All data processing is done locally; only AI requests are sent to external APIs
