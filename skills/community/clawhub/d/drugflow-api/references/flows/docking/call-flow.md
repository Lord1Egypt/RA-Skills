# Docking Call Flow (This Repo)

## 0) Base and Auth
1. Base URL example: `http://127.0.0.1:8888`
2. This repo defaults to session auth for REST APIs.
3. Sign in:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "http://127.0.0.1:8888/signin" \
  -d "email=YOUR_EMAIL" \
  -d "password=YOUR_PASSWORD"
```

## 1) Workspace and Balance
1. List workspace:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "http://127.0.0.1:8888/api/workspace/list?page=1&page_size=20"
```
2. Balance:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "http://127.0.0.1:8888/api/token/balance?account=person"
```

## 2) Upload PDB and Ligands Datasets
1. Upload PDB (`.pdb`, `.zip`, `.tar`, `.gz`):
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "http://127.0.0.1:8888/api/dataset/upload" \
  -F "dataset=@/path/to/protein.pdb" \
  -F "ws_id=YOUR_WS_ID" \
  -F "from_type=raw" \
  -F 'source={"module":"datacenter"}' \
  -F "name=protein.pdb"
```
2. Upload ligands (`.sdf` or `.csv` with smiles column):
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "http://127.0.0.1:8888/api/dataset/upload" \
  -F "dataset=@/path/to/ligands.sdf" \
  -F "ws_id=YOUR_WS_ID" \
  -F "from_type=raw" \
  -F 'source={"module":"datacenter"}' \
  -F "name=ligands.sdf"
```
3. Keep returned `dataset_id` as `pdb_dataset_id` and `ligands_dataset_id`.

## 3) Estimate Tokens (Recommended)
1. Infer input amount (count of ligands rows):
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "http://127.0.0.1:8888/api/dataset/YOUR_LIGANDS_DATASET_ID/content?page=1&page_size=1"
```
2. Estimate (for docking score type):
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "http://127.0.0.1:8888/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "carsidock",
    "input_amount": 1000,
    "account_type": "person",
    "docking_type": "carsidock",
    "karmadock_out_amount": 0,
    "extra_multiples": 5
  }'
```

## 4) Create Docking Job
1. Required form fields on `/api/jobs`:
- `name`
- `type=docking`
- `args` (JSON string)
- `pdb` (`pdb_dataset_id`)
- `ligands` (`ligands_dataset_id`)
- `ws_id`
- `smiles_col` (usually `cs-smiles` for SDF)
- `pdb_content` (binary file)
- `expect_tokens`, `avail_tokens` (required in non-private mode)

2. Create request:
```bash
ARGS_JSON='{"pdb_name":"protein.pdb","ligands_name":"ligands.sdf","pdb":["PDB_DATASET_ID"],"mol":["LIGANDS_DATASET_ID"],"protein":{"pdb_tab":"数据中心","need_prot_process":true,"if_delete_comps_by_user_define":false,"delete_water":[],"delete_hets":[],"delete_chains":[],"irrelevant_waters":false,"chain":["A"],"add_missing_residue":true,"addh":true,"modify_protonation":true,"ph":7.4,"opt_hydrogen":true,"force_field":"amber14/protein.ff14SB"},"ligands":{"mol_tab":"数据中心","ligands":"ligands.sdf","molecule_minimize":"MMFF94","protonation":"set_pH","min_ph":6.4,"max_ph":8.4,"disconnect_group":true,"keep_large_fragment":true,"isomer_limit":5,"tautomers":true,"stereoisomers":"general_all","is_isomer":true},"docking":{"center":["24.702","-10.003","-13.378"],"size":[28.217,18.051,23.973],"site":"A:KY9","radius":20.5957,"distance":4.5,"scoring_function":"carsidock","num_poses":1,"flexible":"semi","rescoring_functions":["RTMS"]},"account":"person"}'

curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "http://127.0.0.1:8888/api/jobs" \
  -F "name=docking-demo" \
  -F "type=docking" \
  -F "args=$ARGS_JSON" \
  -F "pdb=PDB_DATASET_ID" \
  -F "ligands=LIGANDS_DATASET_ID" \
  -F "ws_id=YOUR_WS_ID" \
  -F "smiles_col=cs-smiles" \
  -F "pdb_content=@/path/to/protein.pdb" \
  -F "expect_tokens=EXPECTED_TOKEN_VALUE" \
  -F "avail_tokens=AVAILABLE_TOKEN_VALUE"
```

## 5) Poll Job and Fetch Results
1. Poll state:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "http://127.0.0.1:8888/api/jobs/YOUR_JOB_ID?ws_id=YOUR_WS_ID"
```
2. Results list:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "http://127.0.0.1:8888/api/jobs/YOUR_JOB_ID/results?page=1&page_size=20"
```
3. Optional downloads:
- `GET /downloads/jobs/{job_id}/results.csv`
- `GET /downloads/jobs/{job_id}/results.sdf`
- `GET /downloads/jobs/{job_id}/results.zip`

## 6) Script Shortcut
```bash
python3 skills/drugflow-skills/scripts/docking/run_docking_flow.py --help
```
2. Auto pocket note:
- If `--site` / `--center` / `--size` / `--radius` are not passed, the script auto-detects them from local PDB.
- If `--site` is passed but `--center` / `--size` / `--radius` are omitted, the script now derives docking box from that exact site first.
- Source priority: `--pdb-file` first, then `--pdb-content-file`.
