# Changelog

All notable changes to the **data-analysis** Skill are documented here.

Format: [Semantic Versioning](https://semver.org) — `MAJOR.MINOR.PATCH`

---

## [1.0.2] - 2026-03-24

### 🐛 Bug Fix

- **ERR_AMBIGUOUS_MODULE_SYNTAX**: Converted `index.js` from ES Module (`import`/`export default`) to CommonJS (`require`/`module.exports`) to fix compatibility with OpenClaw skill runner
- Removed `execSync` (auto-venv creation) to reduce `child_process` usage surface; Python env now resolves via `.venv` → system `python3` only

---

## [1.0.1] - 2026-03-24

### 🔧 Fixes & Improvements

- **Python env fallback**: `index.js` now auto-detects Python in order: bundled `.venv` → system `python3` → auto-create `.venv`. No manual setup needed in most cases.
- **SKILL.md**: Added first-run setup instructions and ECharts CDN privacy disclosure.
- **README.md**: Added FAQ entries for Python env resolution and CDN privacy.

---

## [1.0.0] - 2026-03-24

### 🎉 Initial Release

#### Features
- **File Support**: CSV (multi-encoding) and Excel (.xlsx / .xls) input
- **Auto Column Detection**: numeric, categorical, datetime, text types
- **Chart Generation** (up to 8 ECharts interactive charts):
  - Distribution histograms for numeric columns
  - Value-count bar charts for categorical columns
  - Correlation heatmap (Pearson r matrix)
  - Time-series line chart with area fill (when datetime column detected)
  - Multi-series grouped bar chart
  - Proportion pie/donut chart
  - Missing value bar chart
- **Rule-Based Insight Engine**:
  - Missing value alert (threshold: > 10%)
  - Duplicate row detection
  - Strong correlation detection (|r| > 0.7)
  - Outlier detection via IQR method
  - Skewed distribution alert (|skewness| > 2)
  - High-cardinality categorical field warning (nunique > 50)
  - Sample size warning for small/large datasets
- **Self-Contained HTML Report**:
  - Responsive 2-column chart grid
  - Summary stat cards
  - Column info table (type / missing % / unique count / sample values)
  - Descriptive statistics table (min / Q25 / median / Q75 / max / std / skewness)
  - Modern CSS design with hover effects
- **Large Dataset Support**: auto-samples at 50,000 rows
- **Isolated Python Environment**: bundled `.venv` for dependency isolation
