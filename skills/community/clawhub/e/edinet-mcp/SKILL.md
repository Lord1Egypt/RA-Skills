---
name: edinet-mcp
description: "Analyze Japanese public company financial statements (BS/PL/CF/財務諸表) from EDINET (FSA/金融庁) — search by company name or stock code, screen companies, compare periods (xbrl-diff). XBRL data, J-GAAP/IFRS/US-GAAP. Japan securities filings."
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["edinet-mcp"],"env":["EDINET_API_KEY"]},"install":[{"id":"uv","kind":"uv","package":"edinet-mcp","bins":["edinet-mcp"],"label":"Install edinet-mcp (uv)"}],"tags":["japan","finance","edinet","xbrl","financial-statements","mcp","securities","disclosure"]}}
---

# EDINET: Japanese Financial Statement Analysis

Search Japanese public companies and analyze their financial statements via EDINET (金融庁 電子開示システム). Supports income statements (PL/損益計算書), balance sheets (BS/貸借対照表), and cash flow statements (CF/キャッシュ・フロー計算書) with 161 normalized labels across J-GAAP, IFRS, and US-GAAP.

## Use Cases

- Look up any Japanese public company by name or stock code (証券コード)
- Retrieve and compare income statements across companies
- Analyze balance sheet composition and trends
- Review cash flow patterns (operating, investing, financing)
- Compare financials across different accounting standards (J-GAAP/IFRS/US-GAAP)
- Screen multiple companies by ROE, profit margins, and other metrics

## Commands

### Search companies
```bash
# Search by company name (Japanese or English)
edinet-mcp search トヨタ
edinet-mcp search ソニー

# Search by stock code
edinet-mcp search 7203 --limit 5 --json-output
```

### Financial statements
```bash
# Income statement for Toyota (E02144), filed in 2024
edinet-mcp statements -c E02144 -p 2024 -s income_statement --format json

# Balance sheet
edinet-mcp statements -c E02144 -p 2024 -s balance_sheet --format json

# Cash flow statement
edinet-mcp statements -c E02144 -p 2024 -s cash_flow_statement --format json

# All statements as CSV
edinet-mcp statements -c E02144 -p 2024 --format csv
```

### Screen companies (compare metrics)
```bash
# Compare Toyota, Sony, Honda by financial metrics
edinet-mcp screen E02144 E01777 E02529

# Sort by ROE
edinet-mcp screen E02144 E01777 E02529 --sort-by ROE

# JSON output
edinet-mcp screen E02144 E01777 --format json
```

### Test connectivity
```bash
edinet-mcp test
```

### Statement types

| Type | Japanese | Key items |
|---|---|---|
| `income_statement` | 損益計算書 (PL) | 売上高, 営業利益, 純利益 |
| `balance_sheet` | 貸借対照表 (BS) | 総資産, 純資産, 負債 |
| `cash_flow_statement` | CF計算書 | 営業CF, 投資CF, 財務CF |

## Workflow

1. `edinet-mcp search <company>` → find EDINET code
2. `edinet-mcp statements -c <code> -p <year>` → view financial data
3. `edinet-mcp screen <code1> <code2> ...` → compare multiple companies

## Important

- The `-p` (period) parameter is the **filing year**, not the fiscal year. March-end companies file in June of the next year: FY2023 data → `-p 2024`.
- 161 normalized labels across J-GAAP / IFRS / US-GAAP.
- Results include 当期 (current) and 前期 (prior) periods.
- Rate-limited to 0.5 req/sec by default. Screening 10 companies takes ~1-2 minutes.
- Maximum 20 companies per screen request.

## Setup

- Requires `EDINET_API_KEY` environment variable
- Free API key: https://disclosure2dl.edinet-fsa.go.jp/
- Python package: `pip install edinet-mcp` or `uv tool install edinet-mcp`
