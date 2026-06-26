# Molecular Factory Call Flow (This Repo)

## 0) Base and Auth
1. Base URL example: `https://new.drugflow.com`
2. Session auth by `/signin`:
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

## 2) Optional Atom-Selection Helper APIs
For `selected_atoms/start_atoms` confirmation:

1. Atom list from SDF:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/toolkits/rdkit/mol_atom_info" \
  -F "sdf=@/path/to/ligand.sdf"
```

2. Extract partial ligand from selected atoms:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/toolkits/rdkit/extract_partial_mol" \
  -F "sdf=@/path/to/ligand.sdf" \
  -F 'selected_atoms=[1,2,3,4]'
```

3. Optional pocket sanity check:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/molfactory/check_pocket" \
  -d "pdb_dataset_id=PDB_DATASET_ID" \
  -d "ligand_dataset_id=LIGAND_DATASET_ID" \
  -d "center_coord=[-15.459,7.496,-14.396]" \
  -d "box_sizes=[22.736,17.646,23.98]"
```

## 3) Estimate Tokens (Recommended)
Molecular factory token estimate uses `task_type=molfactory`, `input_amount=gen_num`:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/token/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "molfactory",
    "input_amount": 20,
    "account_type": "person",
    "docking_type": "molfactory",
    "karmadock_out_amount": 0,
    "extra_multiples": 1
  }'
```

## 4) Create Molecular Factory Job
1. Endpoint: `POST /api/jobs`
2. Default profile in this skill: **non-docking molecular factory**
- set `args.need_docking=false`
- set all `args.pdb_use.*=false`
- set `args.molgen_algos=["Frag-GPT","REINVENT"]`
- only enable docking fields when user explicitly asks for docking
3. Required form fields:
- `name`
- `type=molecular_factory`
- `args` (JSON string)
- `ws_id`
- `expect_tokens`, `avail_tokens` (required in non-private mode)
4. File fields (conditional):
- `pdb_file`: required when `need_docking=true` or any `pdb_use.*=true`
- `pdb_file`: also required when `ori_ligand_from=pocket`
- if no actual PDB file is uploaded, keep multipart key with empty value `pdb_file=""`
- `ori_ligand`: required when `ori_ligand_from=file`
- `ligands_file_for_docking`: required when `data_from=upload`
- `ligands_file_for_train`: optional

Example:
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  -X POST "https://new.drugflow.com/api/jobs" \
  -F "name=molfactory-demo" \
  -F "type=molecular_factory" \
  -F "args=$(cat /path/to/molfactory_args.json)" \
  -F "ws_id=YOUR_WS_ID" \
  -F "expect_tokens=EXPECTED_TOKEN_VALUE" \
  -F "avail_tokens=AVAILABLE_TOKEN_VALUE" \
  -F "pdb_file=" \
  -F "ori_ligand=@/path/to/ligand.sdf"
```

## 5) Poll Job
```bash
curl -sS -c /tmp/drugflow.cookies -b /tmp/drugflow.cookies \
  "https://new.drugflow.com/api/jobs/YOUR_JOB_ID?ws_id=YOUR_WS_ID"
```

## 6) Script Shortcuts
```bash
python3 skills/drugflow-skills/scripts/molecular-factory/run_molecular_factory_flow.py --help
python3 skills/drugflow-skills/scripts/molecular-factory/run_molecular_factory_flow.py ... atom-info --sdf-file ligand.sdf
python3 skills/drugflow-skills/scripts/molecular-factory/run_molecular_factory_flow.py ... extract-partial --sdf-file ligand.sdf --selected-atoms 1,2,3
python3 skills/drugflow-skills/scripts/molecular-factory/run_molecular_factory_flow.py ... draw-atom-index --sdf-file ligand.sdf --output /tmp/ligand_atom_index.png
python3 skills/drugflow-skills/scripts/molecular-factory/run_molecular_factory_flow.py ... create-job --args-file /path/to/molfactory_args.json --ori-ligand-file ligand.sdf
# add --pdb-file only when docking or pocket-ligand mode requires it
```
