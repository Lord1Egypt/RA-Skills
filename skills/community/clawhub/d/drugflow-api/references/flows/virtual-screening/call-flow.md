# DrugFlow API Call Flow (This Repo)

## 0) Base and Auth
1. Base URL example: `https://new.drugflow.com`
2. This repo's default REST auth is session-based (`/signin` cookie session).
3. Use a cookie jar for command-line calls:
```bash
BASE_URL="https://new.drugflow.com"
COOKIE_JAR="/tmp/drugflow.cookies"
```

## 1) Register or Sign In
1. Sign in (recommended for automation):
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "$BASE_URL/signin" \
  -d "email=YOUR_EMAIL" \
  -d "password=YOUR_PASSWORD"
```
2. Sign up (standard):
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "$BASE_URL/signup" \
  -d "email=YOUR_EMAIL" \
  -d "name=YOUR_NAME" \
  -d "organization=YOUR_ORG" \
  -d "password1=YOUR_PASSWORD" \
  -d "password2=YOUR_PASSWORD"
```
3. Sign up notes:
- `signup` and `signup_for_gpt` may create inactive users until activation link is used.
- For immediate API execution, use an existing active account.

## 2) Workspace
1. List workspace:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  "$BASE_URL/api/workspace/list?page=1&page_size=20"
```
2. Create workspace:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "$BASE_URL/api/workspace/create" \
  -H "Content-Type: application/json" \
  -d '{"ws_name":"codex-vs-workspace","is_default":true}'
```
3. Keep returned `ws_id` for all `/api/jobs` calls.

## 3) Balance and Job List
1. Balance:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  "$BASE_URL/api/token/balance?account=person"
```
2. List jobs by workspace:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  "$BASE_URL/api/jobs?ws_id=YOUR_WS_ID&page=1&page_size=20"
```

## 4) Prepare VS Inputs
1. Fetch in-use virtual screening DBs:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" "$BASE_URL/api/vs/databases"
```
2. Ensure you already have a protein dataset id (`protein_file`), usually from a prior dataset upload in workspace.

## 5) Estimate Tokens (Recommended)
1. `/api/jobs` creation in non-private mode requires client-provided `expect_tokens` and `avail_tokens`.
2. Estimate for VS:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "$BASE_URL/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "vs_karmadock",
    "input_amount": 4317,
    "account_type": "person",
    "docking_type": "carsidock",
    "karmadock_out_amount": 50,
    "extra_multiples": 1
  }'
```

## 6) Create Virtual Screening Job
1. Send form fields: `name`, `type=virtual_screening`, `args` (JSON string), `ws_id`, `expect_tokens`, `avail_tokens`.
2. Example (compact):
```bash
ARGS_JSON='{"pdb":["YOUR_PROTEIN_DATASET_ID"],"pdb_name":"YOUR_PROTEIN.pdb","input_type":"db","input_source":["repurposing"],"input_source_labels":["Drug Repurposing Compound Library(4317)"],"protein":{"protein_file":"YOUR_PROTEIN_DATASET_ID","site":"A:KY9","site_label":"A:KY9:601","center":["24.702","-10.003","-13.378"],"size":[28.217,18.051,23.973],"radius":20.5957},"steps":[{"id":1,"type":"admet","args":{"filter":[{"name":"MW","rules":[{"condition":"gt","value":300},{"condition":"lt","value":400}]},{"name":"TPSA","rules":[{"condition":"gt","value":0},{"condition":"lt","value":140}]},{"name":"LogS","rules":[{"condition":"gt","value":-4},{"condition":"lt","value":0.5}]},{"name":"LogP","rules":[{"condition":"gt","value":1},{"condition":"lt","value":3}]}]},"step":"step1"},{"id":2,"type":"karmadock","args":{"outpose":1,"filter":{"type":"top","order":"desc","expect":{"condition":"ge","value":100}}},"step":"step2"},{"id":3,"type":"carsidock","isomers":false,"args":{"outpose":1,"filter":{"type":"top","order":"desc","expect":{"condition":"ge","value":100}}},"step":"step3"}],"account":"person"}'

curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  -X POST "$BASE_URL/api/jobs" \
  --data-urlencode "name=vs-demo" \
  --data-urlencode "type=virtual_screening" \
  --data-urlencode "args=$ARGS_JSON" \
  --data-urlencode "ws_id=YOUR_WS_ID" \
  --data-urlencode "expect_tokens=EXPECTED_TOKEN_VALUE" \
  --data-urlencode "avail_tokens=AVAILABLE_TOKEN_VALUE"
```

## 7) Poll Job and Fetch Results
1. Poll job:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  "$BASE_URL/api/jobs/YOUR_JOB_ID?ws_id=YOUR_WS_ID"
```
2. Fetch VS result list:
```bash
curl -sS -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
  "$BASE_URL/api/vs/YOUR_JOB_ID/results?page=1&page_size=20"
```
3. Optional VS endpoints:
- `GET /api/vs/{job_id}/agg_results?page=1&page_size=20`
- `POST /api/vs/specify_smiles` with `{"job_id":123,"display_number":1}`
- `GET /download/vs/{job_id}/csv|sdf|pdb|zip`

## 8) Script Shortcut
Run the bundled script for this flow:
```bash
python3 skills/drugflow-skills/scripts/virtual-screening/run_vs_flow.py --help
```
