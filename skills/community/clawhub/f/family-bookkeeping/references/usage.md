# Family Bookkeeping Usage

Use this file for practical command examples, runtime notes, and operator-facing usage details.

## Default Ledger Configuration

Default ledger information should be read from `~/.openclaw/workspace/.env`:

- `FAMILY_BOOKKEEPING_APP_TOKEN`
- `FAMILY_BOOKKEEPING_TABLE_ID`
- `FAMILY_BOOKKEEPING_BITABLE_URL`

## Environment Variables

Feishu credentials and default ledger settings are expected from environment variables:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FAMILY_BOOKKEEPING_APP_TOKEN`
- `FAMILY_BOOKKEEPING_TABLE_ID`
- `FAMILY_BOOKKEEPING_BITABLE_URL`

In most cross-channel runs, explicit `--app-id` / `--app-secret` flags are unnecessary when the environment is already configured.

## Current Capabilities

### 1. Bill import
Supports:
- WeChat bill `.xlsx`
- Alipay bill `.csv`
- Password-protected Alipay `.zip` after extraction

Pipeline:
1. `scripts/normalize_bills.py`
2. `scripts/import_precheck.py`
3. `scripts/export_feishu_import_csv.py`
4. `scripts/write_feishu_records.py`
5. `scripts/import_bills_pipeline.py`

Properties:
- Pre-import dedupe
- Batch import skips rows where `金额 = 0`
- Prefer dedupe by `流水号`
- Fallback dedupe key: `日期 + 金额 + 支付平台 + 备注`
- `--write` performs actual Feishu writes

### 2. Query and reporting
Supports:
- Monthly / specified-month summary
- Breakdown by platform
- Breakdown by first-level / second-level category
- Recent N records
- Reading directly from the live Bitable

### 3. Manual bookkeeping (MVP)
Supports:
- Single-record creation
- Simple date words: `今天 / 昨天 / 前天`
- Simple category inference such as 餐饮 / 交通
- Batch manual backfill after structured generation

### 4. Update one record (MVP)
Supports:
- Locating a record by `备注关键词 + 日期 + 金额`
- Direct update when exactly one record matches
- Returning candidates instead of guessing when multiple matches exist

## Common Commands

### Normalize a bill

```bash
python3 skills/family-bookkeeping/scripts/normalize_bills.py bill.xlsx \
  --bookkeeper 张三 \
  --format json \
  --output normalized.json
```

### Import precheck

```bash
python3 skills/family-bookkeeping/scripts/import_precheck.py normalized.json \
  --app-token "$FAMILY_BOOKKEEPING_APP_TOKEN" \
  --table-id "$FAMILY_BOOKKEEPING_TABLE_ID" \
  --output-dir ./precheck-out
```

### Full import pipeline

```bash
python3 skills/family-bookkeeping/scripts/import_bills_pipeline.py bill.xlsx \
  --bookkeeper 张三
```

If the input is already normalized (`.json/.csv`):

```bash
python3 skills/family-bookkeeping/scripts/import_bills_pipeline.py normalized.json \
  --normalized-input
```

Explicitly write into Feishu:

```bash
python3 skills/family-bookkeeping/scripts/import_bills_pipeline.py bill.xlsx \
  --bookkeeper 张三 \
  --write
```

### Live queries

```bash
python3 skills/family-bookkeeping/scripts/bookkeeping_query_live.py --month 2026-03
```

```bash
python3 skills/family-bookkeeping/scripts/recent_records.py --limit 10
```

### Add one manual record

```bash
python3 skills/family-bookkeeping/scripts/add_manual_record.py "今天中午午餐吃烧鸭饭" --amount 28
```

### Update one record

```bash
python3 skills/family-bookkeeping/scripts/update_record_mvp.py \
  --note-keyword 烧鸭饭 \
  --on-date 2026-04-03 \
  --set-amount 26
```

## Dedupe Rules

Priority:
1. `流水号`
2. `日期 + 金额 + 支付平台 + 备注`

## Verified Capabilities

- Importing WeChat bills into the shared main ledger
- Importing Alipay bills into the shared main ledger
- Importing extracted Alipay ZIP statements
- Live Bitable queries and summary reporting
- Natural-language single-entry bookkeeping
- Recent-record lookup
- Simple record updates
- Batch manual backfill

## Notes

- Delete-one-record is not yet packaged as a reusable script
- Current classification is still lightweight rule-based rather than full NLU
- Housing and home-use spending should be normalized under `生活缴费` rather than using `居住` as a first-level category
- If classification is uncertain, prefer `其他 / 暂未分类`
- Placeholder blank rows in the target Bitable are skipped by `import_precheck.py` and should not count as duplicates
