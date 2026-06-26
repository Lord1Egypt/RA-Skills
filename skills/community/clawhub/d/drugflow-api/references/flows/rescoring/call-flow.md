# Rescoring Call Flow (This Repo)

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

## 2) Prepare Input Datasets
Rescoring (`mode=semi`) requires two input files and uploads them as datasets:
1. protein `*.pdb`
2. ligands `*.sdf`

Upload examples:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/dataset/upload" \
  -F "dataset=@/path/to/protein.pdb" \
  -F "ws_id=YOUR_WS_ID" \
  -F "from_type=raw" \
  -F 'source={"module":"datacenter"}' \
  -F "name=protein.pdb"
```

```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/dataset/upload" \
  -F "dataset=@/path/to/ligands.sdf" \
  -F "ws_id=YOUR_WS_ID" \
  -F "from_type=raw" \
  -F 'source={"module":"datacenter"}' \
  -F "name=ligands.sdf"
```

## 3) Estimate Tokens (Recommended)
1. Get ligand amount:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/dataset/YOUR_LIGANDS_DATASET_ID/content?page=1&page_size=1"
```
2. Estimate rescoring tokens:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "rescoring",
    "input_amount": 1000,
    "account_type": "person",
    "docking_type": "rescoring",
    "karmadock_out_amount": 0,
    "extra_multiples": 1
  }'
```

## 4) Create Rescoring Job
1. Required form fields on `/api/jobs`:
- `name`
- `type=rescoring`
- `args` (JSON string)
- `pdb`
- `ligands`
- `smiles_col`
- `ws_id`
- `expect_tokens`, `avail_tokens` (required in non-private mode)

2. Create request:
```bash
ARGS_JSON='{"mode":"semi","rescoring_functions":["RTMS"],"account":"person"}'

curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/jobs" \
  --data-urlencode "name=rescoring-demo" \
  --data-urlencode "type=rescoring" \
  --data-urlencode "args=$ARGS_JSON" \
  --data-urlencode "pdb=YOUR_PDB_DATASET_ID" \
  --data-urlencode "ligands=YOUR_LIGANDS_DATASET_ID" \
  --data-urlencode "smiles_col=cs-smiles" \
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
python3 skills/drugflow-skills/scripts/rescoring/run_rescoring_flow.py --help
```

Script constraints:
1. `--pdb-file` is required and must be `.pdb`
2. `--ligands-file` is required and must be `.sdf`
