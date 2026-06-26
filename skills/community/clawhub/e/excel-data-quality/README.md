# Excel Data Helper — Data Quality Diagnosis & Chart Skill

> **Fully local** Excel/CSV data overview, quality diagnosis, and charting — no API key needed.

A skill for [OpenClaw](https://openclaw.com) and other AI agents that provides comprehensive data quality analysis and charting capabilities, powered entirely by local Node.js tools.

---

## What Can It Do?

### 1. Quality Check (22 Scan Modules, 6-Dimension Scoring, LLM Semantic Analysis)
Upload a CSV/Excel file and get a complete data profile (column types, null rates, unique values, patterns, statistics) plus a quality scan across six dimensions:
- **Completeness**: null values, empty strings, empty rows, merged cell patterns
- **Accuracy**: outliers (IQR), rare values, value uniformity (zero-variance / dominant value)
- **Consistency**: mixed types, case issues, date formats, full-width/half-width chars, numbers with embedded units, cross-column logical checks
- **Validity**: email/phone format (intl.), special characters, range checks, encoding/mojibake detection, ID card checksum validation
- **Uniqueness**: duplicate rows, primary key violations, near-duplicate (fuzzy) value detection with Unicode normalization
- **Timeliness**: future dates, abnormally old dates

**International locale support**: multilingual field name recognition (EN, ZH, JA, KO, ES, FR, DE, AR), international date formats (ISO, EU DD.MM.YYYY, US MM/DD/YYYY, CJK 年月日, Korean 년월일, Japanese era), global currency symbols (¥ $ € £ ₩ ₹ ₽ etc.), and region-specific quality patterns.

Plus LLM-powered semantic analysis: synonym detection (cross-language), multi-value cells, business key analysis, cross-column relationship insights, locale-specific observations, and data fitness assessment.

Get a weighted quality score (0-100) with grade, breakdown, and actionable recommendations.

### 2. Charts
Generate PNG chart images (server-side ECharts rendering):
- Any ECharts chart type: bar, line, pie, scatter, area, radar, boxplot, heatmap, funnel, treemap, combo, and more
- LLM analyzes data and determines the best 1–5 charts with optimal types and configs
- PNG images sent directly in conversation — no browser needed

### 3. Advanced Charts (via ChartGen)
For dashboards, Gantt charts, diagrams, and PPT — delegates to the ChartGen skill (requires API key).

---

## Installation

### Natural Language Install (OpenClaw)

> Install this skill for me: `https://github.com/excel-data-helper/excel-data-helper-skill.git`

### Manual Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/excel-data-helper/excel-data-helper-skill.git
cd excel-data-helper-skill
npm install
```

---

## Usage Examples

### Quality Check
> "What's in this Excel file?"
> "Check the data quality of this file"
> "Are there any problems with my data?"

### Charts
> "Create a bar chart of sales by category"
> "Suggest some charts for this data"

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/excel_parser.js` | Parse CSV/Excel files, show structure |
| `tools/quality_scanner.js` | Data profiling + 22-module quality scan with scoring |
| `tools/chart_renderer.js` | Data inspection (`--info`) + render any ECharts chart to PNG (`--config`) |

All tools are CLI scripts that output JSON. Run any tool without arguments to see usage help.

---

## Requirements

- **Node.js** >= 14
- **npm** dependencies: `xlsx` (SheetJS), `echarts`, `sharp` — installed via `npm install`
- No API keys, no external services, no internet required

---

## Architecture

```
SKILL.md (main menu)
├── references/quality-check.md      → tools/quality_scanner.js
├── references/chart.md              → tools/chart_renderer.js
└── references/advanced-chart.md     → ChartGen skill (external)
```

Shared libraries in `tools/lib/`: parser, profiler, scanner, scorer, utils.
