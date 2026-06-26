---
name: finance-analyzer
description: This skill should be used when a user needs to analyze financial statements (Income Statement, Balance Sheet, Cash Flow Statement) from Excel or CSV files. It extracts financial data and calculates key metrics such as ROE, ROA, gross margin, and net margin. Trigger scenarios include requests like "analyze this financial report", "calculate ROE/ROA", "what's the gross margin", or any task involving reading and interpreting financial spreadsheets.
---

# Finance Analyzer

## Overview

This skill enables reading and analyzing financial statements from Excel (.xlsx/.xls) and CSV files. It understands the structure of Income Statements (损益表), Balance Sheets (资产负债表), and Cash Flow Statements (现金流量表), extracts key line items, and calculates core financial metrics including ROE, ROA, gross margin (毛利率), and net margin (净利率).

## Workflow

### Step 1: Identify the Input File

Confirm the user has provided or referenced an Excel/CSV file containing financial statements. Supported formats:
- `.xlsx` / `.xls` (Excel workbook, may contain multiple sheets)
- `.csv` (single sheet)

If the user has not provided a file, ask them to provide the financial statement file.

### Step 2: Install Dependencies

Before running the analysis script, ensure required Python packages are available:

```bash
pip install pandas openpyxl
```

### Step 3: Run the Analysis Script

Execute the bundled analysis script to parse the financial data and calculate metrics:

```bash
python3 {SKILL_DIR}/scripts/analyze_financials.py <file_path>
```

Optional arguments:
- `--sheet <sheet_name>` — Analyze a specific sheet only
- `--output <output.json>` — Save results to a JSON file

The script automatically:
1. Detects sheet types (Income Statement, Balance Sheet, Cash Flow) by sheet name keywords
2. Falls back to content-based detection if sheet names are ambiguous
3. Extracts key financial line items using Chinese and English keyword matching
4. Calculates all available metrics from the extracted data

### Step 4: Interpret and Present Results

After running the script, interpret the JSON output for the user. The output contains:

- **`parsed_data`**: Raw extracted values from each statement type
- **`metrics`**: Calculated financial metrics with values, formulas, and component breakdowns
- **`warnings`**: Any data items that could not be found or calculated

When presenting results to the user:

1. **Display the core metrics** the user requested (typically ROE, ROA, gross margin, net margin) in a clear table format
2. **Show the calculation formula and components** so the user can verify the numbers
3. **Flag any warnings** — explain which metrics could not be calculated and why (e.g., missing data)
4. **Provide professional interpretation** — reference `references/financial_statements_guide.md` for benchmark ranges and contextual analysis

Example output format:

```
| 指标 | 数值 | 公式 |
|------|------|------|
| ROE（净资产收益率） | 18.5% | 净利润 / 股东权益 × 100% |
| ROA（总资产收益率） | 8.2% | 净利润 / 总资产 × 100% |
| 毛利率 | 35.6% | 毛利润 / 营业收入 × 100% |
| 净利率 | 12.3% | 净利润 / 营业收入 × 100% |
```

### Step 5: Handle Edge Cases

- **Unrecognized sheet names**: If the script cannot detect sheet types, prompt the user to specify which sheet contains which statement using `--sheet`
- **Missing data**: If key line items cannot be found, read the file directly to inspect the format, then adjust the approach or guide the user
- **Multiple periods**: The script extracts the most recent period's data by default. If the user needs trend analysis across periods, read the file manually and perform the comparison
- **Unit differences**: Check if amounts are in 元, 万元, or 百万元, and normalize if needed before interpretation

## Reference Material

For detailed information about financial statement structures, metric definitions, benchmark ranges, and interpretation guidance, refer to `references/financial_statements_guide.md`. This reference covers:

- Structure of all three financial statements (Chinese and English)
- Core metric formulas and industry benchmarks
- DuPont analysis framework
- Common Excel format patterns and parsing considerations
