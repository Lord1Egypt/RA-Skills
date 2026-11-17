# Enterprise Report Merger

Merge multiple Excel/PDF enterprise reports (financial statements, department budgets, business data tables) into a unified report, and optionally fill the result into a Word template to generate a final formatted report.

## Features

- Read tabular data from Excel (.xlsx/.xls) and PDF files
- Three merge modes:
  - **Simple concatenation**: stack multiple sources vertically
  - **Key-based merge**: match horizontally by account code / department / other key columns
  - **Consolidated reports + elimination entries**: parent-subsidiary group consolidation with intercompany transaction elimination
- Write merged results to formatted Excel files
- Fill merged data into Word (.docx) templates to generate final reports
- Auto-generate a complete analysis report (e.g., post-loan analysis report) when no template is provided
- **18 financial ratios auto-calculated** (4 categories: solvency 7 / operating efficiency 3 / profitability 5 / growth 3, supporting prior-period averages and growth rates)

## Installation

```
npx clawhub@latest install enterprise-report-merger
```

Or import the .zip skill package via WorkBuddy: Skills → Add Skill → Upload Skill.

## Dependencies

```
pip install openpyxl pdfplumber python-docx xlrd PyMuPDF
```

| Dependency | Required for |
|---|---|
| openpyxl | Excel input/output |
| xlrd | Legacy .xls files |
| pdfplumber | PDF table extraction |
| PyMuPDF | Image-based PDF detection |
| python-docx | Word template filling |

## Usage

Trigger the skill by describing your task in natural language:

- "Merge these Excel reports"
- "Combine subsidiary financial statements into a consolidated report"
- "Fill this data into the Word template"
- "Generate a post-loan analysis report without a template"

## Merge Modes

| Mode | Use case |
|---|---|
| Simple concatenation | Multiple sources with the same structure, stacked vertically |
| Key-based merge | Match rows by a key column (e.g., account code, department name) |
| Consolidation + elimination | Parent-subsidiary group consolidation with intercompany elimination |

## License

MIT-0
