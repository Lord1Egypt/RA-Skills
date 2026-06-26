---
name: drugflow-skills
description: Multi-flow API workflow skill for this DrugFlow Django repository. Use when an agent needs executable end-to-end API procedures such as login/register, workspace and balance retrieval, job listing, virtual screening, docking, ADMET, rescoring, structure extraction, and molecular factory.
---

# DrugFlow Skills

Route requests to the correct DrugFlow API flow and execute with minimal ambiguity.

## Flow Selection
1. Read [references/index.md](references/index.md) first.
2. Match user intent to one flow.
3. Load only that flow's reference files.
4. Prefer script execution from `scripts/<flow>/` when available.

## Current Flows
1. Common APIs: reusable auth/workspace/balance/jobs APIs available.
2. Virtual screening: complete flow available.
3. Docking: complete flow available.
4. ADMET: complete flow available.
5. Rescoring: complete flow available.
6. Structure extract: complete flow available (`img2mol` backend type).
7. Molecular factory: complete flow available (with atom-selection helpers).

## Common APIs Workflow
1. Read [references/flows/common-apis/call-flow.md](references/flows/common-apis/call-flow.md).
2. Read [references/flows/common-apis/payloads.md](references/flows/common-apis/payloads.md).
3. Reuse `scripts/common/drugflow_api.py` for:
- `signin`
- `signup`
- `list_workspaces` / `create_workspace` / `ensure_workspace`
- `get_balance`
- `list_jobs`
4. Use `scripts/common/test_common_apis.py` for direct smoke tests.

## Virtual Screening Workflow
1. Read [references/flows/virtual-screening/call-flow.md](references/flows/virtual-screening/call-flow.md).
2. Read [references/flows/virtual-screening/payloads.md](references/flows/virtual-screening/payloads.md).
3. Use `scripts/virtual-screening/run_vs_flow.py` for end-to-end execution.
4. Always include `ws_id` for `/api/jobs` list/detail.
5. For `/api/jobs` create, pass `name`, `type`, `args` (JSON string), `ws_id`; in non-private mode include `expect_tokens` and `avail_tokens`.

## Docking Workflow
1. Read [references/flows/docking/call-flow.md](references/flows/docking/call-flow.md).
2. Read [references/flows/docking/payloads.md](references/flows/docking/payloads.md).
3. Use `scripts/docking/run_docking_flow.py` for end-to-end execution.
4. Create docking jobs through `POST /api/jobs` with multipart fields `pdb`, `ligands`, `pdb_content`, and `args`.
5. Site-driven docking box note: when `--site` is provided but `center/size/radius` are omitted, the script auto-derives the docking box from that site in local PDB.
6. Always include `ws_id` on job list/detail requests and pass `expect_tokens`/`avail_tokens` in non-private mode.

## ADMET Workflow
1. Read [references/flows/admet/call-flow.md](references/flows/admet/call-flow.md).
2. Read [references/flows/admet/payloads.md](references/flows/admet/payloads.md).
3. Use `scripts/admet/run_admet_flow.py` for end-to-end execution.
4. ADMET job type is fixed to `admet-dl`.
5. Support two input modes:
- direct `smiles` list
- dataset mode via `dataset_id + smiles_col`
6. For `/api/jobs` create, pass `name`, `type=admet-dl`, `args`, `ws_id`, and in non-private mode `expect_tokens`/`avail_tokens`.

## Rescoring Workflow
1. Read [references/flows/rescoring/call-flow.md](references/flows/rescoring/call-flow.md).
2. Read [references/flows/rescoring/payloads.md](references/flows/rescoring/payloads.md).
3. Use `scripts/rescoring/run_rescoring_flow.py` for end-to-end execution.
4. Create rescoring jobs through `POST /api/jobs` with:
- `type=rescoring`
- form fields `pdb`, `ligands`, `smiles_col`
- `args.mode=semi` and `args.rescoring_functions`
5. Script enforces input files: `--pdb-file` must be `.pdb`, `--ligands-file` must be `.sdf`.
6. Always include `ws_id`; in non-private mode include `expect_tokens` and `avail_tokens`.

## Structure Extract Workflow
1. Read [references/flows/structure-extract/call-flow.md](references/flows/structure-extract/call-flow.md).
2. Read [references/flows/structure-extract/payloads.md](references/flows/structure-extract/payloads.md).
3. Use `scripts/structure-extract/run_structure_extract_flow.py` for end-to-end execution.
4. User-facing "结构提取" maps to backend job `type=img2mol`.
5. For create, pass `name`, `type=img2mol`, `args` (`dataset_id`, `page_list`), `ws_id`, and in non-private mode `expect_tokens`/`avail_tokens`.
6. `dataset_id` must be img2mol-compatible and include `extras.osskey`.

## Molecular Factory Workflow
1. Read [references/flows/molecular-factory/call-flow.md](references/flows/molecular-factory/call-flow.md).
2. Read [references/flows/molecular-factory/payloads.md](references/flows/molecular-factory/payloads.md).
3. Use `scripts/molecular-factory/run_molecular_factory_flow.py`:
- `atom-info`
- `extract-partial`
- `draw-atom-index`
- `create-job`
4. Default to non-docking molecular factory unless user explicitly asks for docking:
- `args.need_docking=false`
- `args.pdb_use.*=false`
5. Default generation models:
- `args.molgen_algos=["Frag-GPT","REINVENT"]`
6. Use helper APIs first to confirm `selected_atoms/start_atoms`, then submit `molecular_factory` job.
7. Always pass `ws_id`; in non-private mode include `expect_tokens` and `avail_tokens`.

## Output Contract
1. Return method + endpoint + required parameters for each step.
2. Return key ids and state: `ws_id`, `job_id`, `state`, result `count`.
3. When running scripts, return command + important outputs.

## Expansion Rules
1. Add new flow docs under `references/flows/<flow>/` with `call-flow.md` and `payloads.md`.
2. Add runnable scripts under `scripts/<flow>/`.
3. Update [references/index.md](references/index.md) and this file's `Current Flows` section.

## References
1. [references/index.md](references/index.md)
2. [references/flows/common-apis/call-flow.md](references/flows/common-apis/call-flow.md)
3. [references/flows/common-apis/payloads.md](references/flows/common-apis/payloads.md)
4. [references/flows/virtual-screening/call-flow.md](references/flows/virtual-screening/call-flow.md)
5. [references/flows/virtual-screening/payloads.md](references/flows/virtual-screening/payloads.md)
6. [references/flows/docking/call-flow.md](references/flows/docking/call-flow.md)
7. [references/flows/docking/payloads.md](references/flows/docking/payloads.md)
8. [references/flows/admet/call-flow.md](references/flows/admet/call-flow.md)
9. [references/flows/admet/payloads.md](references/flows/admet/payloads.md)
10. [references/flows/molecular-factory/call-flow.md](references/flows/molecular-factory/call-flow.md)
11. [references/flows/molecular-factory/payloads.md](references/flows/molecular-factory/payloads.md)
12. [references/flows/rescoring/call-flow.md](references/flows/rescoring/call-flow.md)
13. [references/flows/rescoring/payloads.md](references/flows/rescoring/payloads.md)
14. [references/flows/structure-extract/call-flow.md](references/flows/structure-extract/call-flow.md)
15. [references/flows/structure-extract/payloads.md](references/flows/structure-extract/payloads.md)
