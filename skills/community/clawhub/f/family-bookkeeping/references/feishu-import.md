# Family Bookkeeping Feishu Import

Use this file for the last-mile Feishu import workflow.

## Current Practical Workflow

Because direct scripted row writes may not always be available in the current runtime/tool surface, prefer this robust fallback:

1. Normalize the source bill file
2. Export a Feishu-importable CSV
3. Import that CSV into the target Bitable through Feishu UI

## Target Ledger

Target ledger configuration should come from `~/.openclaw/workspace/.env`:

- `FAMILY_BOOKKEEPING_APP_TOKEN`
- `FAMILY_BOOKKEEPING_TABLE_ID`
- `FAMILY_BOOKKEEPING_BITABLE_URL`

## Expected Columns for Import CSV

- `家庭记账` (primary field)
- `日期`
- `金额`
- `记账人`
- `一级类型`
- `二级类型`
- `备注`
- `收支类型`
- `支付平台`
- `导入来源`
- `流水号`

## Two-Step CLI Flow

### Step 1: normalize raw bill

```bash
python3 skills/family-bookkeeping/scripts/normalize_bills.py bill.xlsx --bookkeeper Lawliet --format json --output normalized.json
```

### Step 2: export Feishu import CSV

```bash
python3 skills/family-bookkeeping/scripts/export_feishu_import_csv.py normalized.json --output feishu-import.csv
```

Then import `feishu-import.csv` into the Bitable configured in your environment.

## Import Advice

- Before importing, confirm the column mapping in Feishu UI
- Prefer dedupe by `流水号`
- For repeated imports, check whether the incoming batch overlaps with existing rows
- Keep the original statement file and the normalized JSON as audit artifacts
