# ADMET Call Flow (This Repo)

## 0) Base and Auth
1. Base URL example: `https://new.drugflow.com`
2. REST API uses session auth (`/signin`) by default.
3. Sign in:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/signin" \
  -d "email=YOUR_EMAIL" \
  -d "password=YOUR_PASSWORD"
```

## 1) Workspace and Balance
1. Workspace list:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/workspace/list?page=1&page_size=20"
```
2. Balance:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/token/balance?account=person"
```

## 2) Input Mode
ADMET supports two input modes:
1. Direct smiles list (form field `smiles`, JSON array string)
2. Dataset reference (`args.dataset_id` + `args.smiles_col`)

Dataset count (for token estimation):
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/dataset/YOUR_DATASET_ID/content?page=1&page_size=1"
```

## 3) Estimate Tokens (Recommended)
1. ADMET task-type mapping for `/api/token/estimate`:
- `admet-dl` + `sme=false` -> `admet_mert`
- `admet-dl` + `sme=true` -> `admet_mga`
2. Example:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "admet_mert",
    "input_amount": 1000,
    "account_type": "person",
    "docking_type": "admet_mert",
    "karmadock_out_amount": 0,
    "extra_multiples": 1
  }'
```

## 4) Create ADMET Job
1. Required top-level form fields on `/api/jobs`:
- `name`
- `type=admet-dl`
- `args` (JSON string)
- `ws_id`
- `expect_tokens`, `avail_tokens` (required in non-private mode)
2. Input requirement:
- direct smiles: include form field `smiles='["CCO","CCN"]'`
- dataset mode: include `dataset_id` and `smiles_col` inside `args`

Example (dataset mode):
```bash
ARGS_JSON='{"dataset_id":"YOUR_DATASET_ID","smiles_col":"cs-smiles","account":"person","sme":false}'

curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/jobs" \
  --data-urlencode "name=admet-demo" \
  --data-urlencode "type=admet-dl" \
  --data-urlencode "args=$ARGS_JSON" \
  --data-urlencode "ws_id=YOUR_WS_ID" \
  --data-urlencode "expect_tokens=EXPECTED_TOKEN_VALUE" \
  --data-urlencode "avail_tokens=AVAILABLE_TOKEN_VALUE"
```

Example (direct smiles mode):
```bash
ARGS_JSON='{"account":"person","sme":true,"is_calc_vis":true}'
SMILES_JSON='["CCO","CCN","c1ccccc1"]'

curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/jobs" \
  --data-urlencode "name=admet-smiles-demo" \
  --data-urlencode "type=admet-dl" \
  --data-urlencode "args=$ARGS_JSON" \
  --data-urlencode "smiles=$SMILES_JSON" \
  --data-urlencode "ws_id=YOUR_WS_ID" \
  --data-urlencode "expect_tokens=EXPECTED_TOKEN_VALUE" \
  --data-urlencode "avail_tokens=AVAILABLE_TOKEN_VALUE"
```

## 5) Poll Job and Query Results
1. Poll state:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/jobs/YOUR_JOB_ID?ws_id=YOUR_WS_ID"
```
2. Query result rows:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/jobs/YOUR_JOB_ID/results?page=1&page_size=20"
```

## 6) Script Shortcut
```bash
python3 skills/drugflow-skills/scripts/admet/run_admet_flow.py --help
```
