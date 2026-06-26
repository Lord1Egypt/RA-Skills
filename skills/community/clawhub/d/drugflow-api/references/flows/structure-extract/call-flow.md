# Structure Extract Call Flow (This Repo)

## 0) Backend Type Mapping
User-facing "结构提取" is implemented by backend job type `img2mol`.

## 1) Base and Auth
1. Base URL example: `https://new.drugflow.com`
2. REST API uses session auth (`/signin`) by default.
3. Sign in:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/signin" \
  -d "email=YOUR_EMAIL" \
  -d "password=YOUR_PASSWORD"
```

## 2) Workspace and Balance
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

## 3) Pick An Img2Mol-Compatible Dataset
`img2mol` requires dataset metadata `extras.osskey`.
In practice this dataset is usually created by frontend structure-extract upload flow (`create_oss` path), then reused by `dataset_id`.

List workspace PDF/image datasets:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/workspace/datalists?ws_id=YOUR_WS_ID&filter=pdf"
```

Check one dataset has `extras_info.osskey`:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/dataset/YOUR_DATASET_ID/metainfo"
```

## 4) Estimate Tokens (Recommended)
Use selected page count as `input_amount`:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "img2mol",
    "input_amount": 3,
    "account_type": "person",
    "docking_type": "img2mol",
    "karmadock_out_amount": 0,
    "extra_multiples": 1
  }'
```

## 5) Create Structure Extract Job
1. Required top-level form fields on `/api/jobs`:
- `name`
- `type=img2mol`
- `args` (JSON string)
- `ws_id`
- `expect_tokens`, `avail_tokens` (required in non-private mode)

2. `args` must include:
- `dataset_id`
- `page_list` (integer list, e.g. `[1,2,3]`)

Example:
```bash
ARGS_JSON='{"dataset_id":"YOUR_DATASET_ID","page_list":[1,2,3],"account":"person"}'

curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/jobs" \
  --data-urlencode "name=img2mol-demo" \
  --data-urlencode "type=img2mol" \
  --data-urlencode "args=$ARGS_JSON" \
  --data-urlencode "ws_id=YOUR_WS_ID" \
  --data-urlencode "expect_tokens=EXPECTED_TOKEN_VALUE" \
  --data-urlencode "avail_tokens=AVAILABLE_TOKEN_VALUE"
```

## 6) Poll Job and Query Results
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
3. Optional exports:
- `GET /download/img2mol/{job_id}`
- `GET /download/img2mol/{job_id}/zip`

## 7) Script Shortcut
```bash
python3 skills/drugflow-skills/scripts/structure-extract/run_structure_extract_flow.py --help
```
