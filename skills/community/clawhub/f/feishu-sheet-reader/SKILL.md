---
name: feishu-sheet-reader
description: Read data from Feishu Sheets (电子表格). Activates when user shares a Feishu spreadsheet/sheet link (feishu.cn/sheets/...), asks to read/scan/look at a sheet, or wants to analyze sheet data. Supports reading specific ranges, entire sheets, and sheet metadata listing. Triggered by: 飞书表格, 飞书sheet, sheets link, 电子表格链接, 读取表格.
---

# Feishu Sheet Reader

Read data from Feishu Sheets (电子表格) via the Feishu API.

## URL Format

Feishu sheet URLs look like:
```
https://my.feishu.cn/sheets/GHOustTi8h4sVPtCFdxcoznknve?sheet=062ee8
```
- `GHOustTi8h4sVPtCFdxcoznknve` = **spreadsheet token** (first path segment after `/sheets/`)
- `062ee8` = **sheet ID** (query param `sheet=`, the tab inside the spreadsheet)

## Script Usage

```bash
python3 scripts/read_feishu_sheet.py <spreadsheet_token> [sheet_id] [range]
```

Examples:
```bash
# Read entire first sheet
python3 scripts/read_feishu_sheet.py GHOustTi8h4sVPtCFdxcoznknve

# Read specific sheet by ID
python3 scripts/read_feishu_sheet.py GHOustTi8h4sVPtCFdxcoznknve 062ee8

# Read specific range (e.g., A1:D10)
python3 scripts/read_feishu_sheet.py GHOustTi8h4sVPtCFdxcoznknve 062ee8 A1:D10
```

Output is tab-separated, suitable for pasting into analysis or reformatting.

## Workflow

1. Parse spreadsheet token and sheet ID from the URL
2. Get Feishu app credentials from gateway config via `openclaw config get`
3. Obtain tenant access token via Feishu Auth API
4. Call Sheets API: `GET /open-apis/sheets/v2/spreadsheets/{token}/values/{range}`
5. Format and return the data

## Sheet ID Detection

If `sheet_id` is omitted, the script queries `/sheets/v2/spreadsheets/{token}/sheets/query` to list all sheets and uses the first one.

## API Reference

- Auth: `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
- Sheet values: `GET https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values/{range}`
- Sheet meta: `GET https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets/query`
