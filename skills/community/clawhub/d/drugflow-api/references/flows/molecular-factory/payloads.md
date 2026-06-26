# Molecular Factory Payload Notes

## `/api/jobs` Required Top-Level Form Fields
1. `name`
2. `type` = `molecular_factory`
3. `args` (JSON string)
4. `ws_id`
5. `expect_tokens`, `avail_tokens` (required in non-private mode)
6. `pdb_file` key should always exist in multipart form:
- upload file when needed
- otherwise pass empty string `""` to avoid backend `request.data["pdb_file"]` key errors

## Conditional File Fields
1. `pdb_file`: required when
- `args.need_docking == true`, or
- any `args.pdb_use` value is `true`
- `args.ori_ligand_from == "pocket"` (backend extracts reference ligand from uploaded PDB)
2. `ori_ligand`: required when `args.ori_ligand_from == "file"`
3. `ligands_file_for_docking`: required when `args.data_from == "upload"`
4. `ligands_file_for_train`: optional (used for fine-tune inputs)
5. `ligands_file_smiles_col`: optional, mainly for CSV train file mode

## Core `args` Keys (Practical Minimum)
1. `need_docking` (bool, default/recommended: `false`)
2. `pdb_use` (dict for each algo)
3. `data_from` (`molgen` or `upload`)
4. `center` (3 floats/strings)
5. `size` (3 floats)
6. `radius` (float)
7. `gen_num` (int)
8. `gen_time` (minutes, int)
9. `molgen_algos` (string list; default/recommended: `["Frag-GPT","REINVENT"]`)
10. `generate_mode` (string)
11. `selected_atoms` (int list; required when `generate_mode != DeNovo`)
12. `start_atoms` (int list; required when `generate_mode != DeNovo`)
13. `ori_ligand_from` (`pocket` or `file`)
14. `ori_ligand_site` (required when `ori_ligand_from == pocket`, e.g. `A:1E8`)
15. `filter_args` (ADMET filter list)
16. `account` (`person` or `team`)
17. `docking` (optional when `need_docking=false`; if `need_docking=true`, include at least `docking.scoring_function`)

## Useful Optional `args` Keys
1. `rmsds`: atom-index groups for RMSD calculation in result callbacks
2. `sites_check`: atom ids for per-result site checks

## Frontend-Heavy Keys (Usually Redundant for Job Execution)
For `/api/jobs` create, these fields are generally UI state and not required by backend scheduling:
1. `is_pocket`, `pdb`, `mol`, `pdb_dataset_id`, `pdb_name`
2. `is_pdb_example`, `is_dock_pdb_example`, `dock_pdb_name`
3. `active_file_name`, `active_dataset_id`, `is_active_sample`
4. `is_reference`, `refer_tab`, `ligand_label`, `ligand_smiles`, `refer_file_name`
5. `isActive`, `is_filterate`, `is_position`, `is_compare`, `box_ligand`
6. `position_val`, `position_options`, `atomPosition_options`, `atomPosition_labels`
7. `show_rmsds`, `ligand_sdf_2d`, `ligand_sdf_3d`

## Recommended Helper Flow for Atom Confirmation
1. `POST /api/toolkits/rdkit/mol_atom_info` -> get `atom_id` / `atom_symbol`
2. Select candidate `selected_atoms` / `start_atoms`
3. `POST /api/toolkits/rdkit/extract_partial_mol` -> inspect fragment smiles/block
4. (Optional) render atom-index image locally for manual review

## Example Minimal Template
```json
{
  "need_docking": false,
  "pdb_use": {
    "3D-linker": false,
    "Diff-linker": false,
    "Frag-GPT": false,
    "Delete": false,
    "REINVENT": false
  },
  "data_from": "molgen",
  "center": ["-15.459", "7.496", "-14.396"],
  "size": [22.736, 17.646, 23.98],
  "radius": 18.7306,
  "gen_num": 20,
  "gen_time": 30,
  "molgen_algos": ["Frag-GPT", "REINVENT"],
  "generate_mode": "Linker-based",
  "selected_atoms": [6, 9, 25, 32, 8, 21, 22, 19],
  "start_atoms": [20, 21],
  "ori_ligand_from": "file",
  "filter_args": [
    {"name": "MW", "min": 300, "max": 800},
    {"name": "TPSA", "min": 0, "max": 160}
  ],
  "account": "person"
}
```

## Common Errors
1. `This task need pdb, but not pdb found`: missing `pdb_file` when docking/global-pdb/pocket-ligand mode requires it
2. `current task must provides ligand file`: missing reference ligand for required mode
3. `selected atoms error` / `start atoms error`: invalid atom index set
4. `Insufficient account balance`: balance smaller than internal `gen_num * molfactory` requirement
5. `${field} must be provided`: missing top-level `/api/jobs` required form fields
