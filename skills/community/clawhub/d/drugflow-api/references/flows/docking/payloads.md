# Docking Payloads (Validated From This Repo)

## `/api/jobs` Required Form Fields
1. `name`
2. `type` = `docking`
3. `args` (JSON string)
4. `pdb` (protein dataset id)
5. `ligands` (ligands dataset id)
6. `ws_id`
7. `smiles_col` (for SDF usually `cs-smiles`)
8. `pdb_content` (binary pdb file)
9. `expect_tokens`, `avail_tokens` (required in non-private mode)

---

## Protein Processing Parameters (`args.protein`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pdb_tab` | string | `"数据中心"` | Source tab label for the protein (Data Center). |
| `need_prot_process` | bool | `true` | Whether to run protein preparation (clean up, add H, etc.). |
| `if_delete_comps_by_user_define` | bool | `false` | If `true`, user-specified HETATM compounds are removed. |
| `delete_water` | array | `[]` | List of water molecules to delete, e.g. `[{"chain_id":"A","residue_number":"401"}]`. |
| `delete_hets` | array | `[]` | List of HETATM groups to remove (ligands/cofactors). Same format as `delete_water`. |
| `delete_chains` | array | `[]` | Chain IDs to remove entirely, e.g. `["B","C"]`. |
| `irrelevant_waters` | bool | `false` | If `true`, remove all waters not in the binding pocket. |
| `chain` | array | `["A"]` | Chains to keep for docking. Typically the chain containing the binding site. |
| `add_missing_residue` | bool | `true` | Rebuild missing residues using PDBFixer / modelling. |
| `addh` | bool | `true` | Add hydrogen atoms. |
| `modify_protonation` | bool | `true` | Adjust protonation states based on pH. |
| `ph` | float | `7.4` | Target pH for protonation (physiological = 7.4). |
| `opt_hydrogen` | bool | `true` | Optimize hydrogen positions after addition. |
| `force_field` | string | `"amber14/protein.ff14SB"` | Force field for energy minimization. Options: `"amber14/protein.ff14SB"`, `"charmm36"`. |

---

## Ligand Preparation Parameters (`args.ligands`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mol_tab` | string | `"数据中心"` | Source tab label for ligands. |
| `ligands` | string | `"ligands.sdf"` | Display name of ligands file. |
| `molecule_minimize` | string | `"MMFF94"` | Force field for ligand energy minimization. Options: `"MMFF94"`, `"UFF"`, `"None"`. |
| `protonation` | string | `"set_pH"` | Protonation mode. `"set_pH"` adds/removes H based on pH range; `"as_is"` keeps original. |
| `min_ph` | float | `6.4` | Lower pH bound for protonation enumeration. |
| `max_ph` | float | `8.4` | Upper pH bound for protonation enumeration. |
| `disconnect_group` | bool | `true` | Break disconnected salt bridges / metal complexes. |
| `keep_large_fragment` | bool | `true` | After disconnect, keep only the largest fragment. |
| `isomer_limit` | int | `5` | Max number of isomers to generate per input molecule. Affects token cost. |
| `tautomers` | bool | `true` | Enumerate tautomers. |
| `stereoisomers` | string | `"general_all"` | Stereoisomer enumeration mode: `"general_all"`, `"general_unspecified"`, `"none"`. |
| `is_isomer` | bool | `true` | Master switch for isomer/tautomer enumeration. |

---

## Docking Parameters (`args.docking`)

### Pocket Definition

These parameters define **where on the protein** docking is performed:

#### `site`
- **Format**: `"<chain>:<ligand_name>"`, e.g. `"A:KY9"`
- **Meaning**: Identifies the binding pocket by the co-crystallised reference ligand. `A` = chain ID, `KY9` = 3-letter PDB residue name of the ligand.
- **How to determine**: Parse PDB HETATM records, find the desired ligand (typically the largest non-water, non-ion ligand), take `chain:residue_name`.

#### `center`
- **Format**: `["x", "y", "z"]` (array of **string** floats, Angstroms)
- **Meaning**: Geometric center of the docking search box.
- **How to determine**: Centroid of the reference ligand's atom coordinates:
  ```
  center_x = (max_x + min_x) / 2
  center_y = (max_y + min_y) / 2
  center_z = (max_z + min_z) / 2
  ```

#### `size`
- **Format**: `[x, y, z]` (array of floats, Angstroms)
- **Meaning**: Dimensions of the search box along x/y/z axes.
- **How to determine**: Bounding box of reference ligand + padding (`expand`, default 10 Å):
  ```
  size_x = (max_x - min_x) + expand
  size_y = (max_y - min_y) + expand
  size_z = (max_z - min_z) + expand
  ```

#### `radius`
- **Format**: float (Angstroms)
- **Meaning**: Spherical search radius from center. Some scoring functions (CARSIDock) use this instead of/alongside the rectangular box.
- **How to determine**: Max distance from any ligand atom to center + half of expand:
  ```
  radius = max(distance(atom_i, center)) + expand / 2
  ```

### Automatic Detection from PDB File

When `--site`/`--center`/`--size`/`--radius` are omitted, `run_docking_flow.py` can auto-detect pocket from local PDB content:
1. Prefer `--pdb-file`.
2. Fallback to `--pdb-content-file` when `--pdb-file` is absent.
3. Then parse pocket using the steps below.

When `--site` is already provided but docking box is incomplete (`center/size/radius` missing), the script first tries to locate that exact site in the local PDB and derives the docking box from it.

Detection steps:
1. All HETATM records are parsed (excluding `HOH` and common ions).
2. Atoms are grouped by `(chain, residue_name, residue_id)`.
3. The group with the **most atoms** (>= 6) is selected as the reference ligand.
4. `site`, `center`, `size`, `radius` are computed from its bounding box.

Usage:
```bash
python3 scripts/docking/run_docking_flow.py \
  --base-url http://127.0.0.1:8888 \
  --email user@example.com --password secret \
  --pdb-file /path/to/protein.pdb \
  --ligands-file /path/to/ligands.sdf \
  --expand 10.0
```

or:
```bash
python3 scripts/docking/run_docking_flow.py \
  --base-url http://127.0.0.1:8888 \
  --email user@example.com --password secret \
  --pdb-dataset-id PDB_DATASET_ID \
  --pdb-content-file /path/to/protein.pdb \
  --ligands-dataset-id LIGANDS_DATASET_ID \
  --expand 10.0
```

Standalone ligand inspection:
```bash
python3 scripts/common/pdb_parser.py /path/to/protein.pdb --list-ligands
```

### Other Docking Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `distance` | float | `4.5` | Interaction distance threshold (Å) — residues within this distance of the ligand are considered part of the binding pocket for flexible docking. |
| `scoring_function` | string | `"carsidock"` | Docking engine / scoring function. See list below. |
| `num_poses` | int | `1` | Number of output docking poses per ligand. More poses = more compute time. |
| `flexible` | string | `"semi"` | Side-chain flexibility: `"none"` (rigid receptor), `"semi"` (flexible side chains near pocket), `"flex"` (full flexible). |
| `rescoring_functions` | array | `["RTMS"]` | Post-docking rescoring methods. `"RTMS"` is the Real-Time Molecular Scoring function for re-ranking. |

---

## Supported `docking.scoring_function`
| Value | Description |
|-------|-------------|
| `carsidock` | CARSIDock — GPU-accelerated deep-learning scoring. High accuracy, recommended default. |
| `carsidock-cov` | CARSIDock covalent mode — for covalent inhibitors that form a bond with a residue (e.g. CYS). |
| `karmadock` | KarmaDock — fast ML-based docking, good for large-scale screening. |
| `vina` | AutoDock Vina — classic empirical scoring, CPU-based. |
| `vina_gpu` | AutoDock Vina GPU — GPU-accelerated Vina variant. |
| `boltz` | Boltz — Boltzmann-weighted sampling approach. |

## Token Estimation Mapping
Use `/api/token/estimate` with:
1. `task_type = docking.scoring_function`
2. `input_amount = ligands count`
3. `extra_multiples = ligands.isomer_limit`

Note: backend docking withholding uses discounted formula with `0.8` factor.

---

## Minimal Stable `args` Template
```json
{
  "pdb_name": "protein.pdb",
  "ligands_name": "ligands.sdf",
  "pdb": ["PDB_DATASET_ID"],
  "mol": ["LIGANDS_DATASET_ID"],
  "protein": {
    "pdb_tab": "数据中心",
    "need_prot_process": true,
    "if_delete_comps_by_user_define": false,
    "delete_water": [],
    "delete_hets": [],
    "delete_chains": [],
    "irrelevant_waters": false,
    "chain": ["A"],
    "add_missing_residue": true,
    "addh": true,
    "modify_protonation": true,
    "ph": 7.4,
    "opt_hydrogen": true,
    "force_field": "amber14/protein.ff14SB"
  },
  "ligands": {
    "mol_tab": "数据中心",
    "ligands": "ligands.sdf",
    "molecule_minimize": "MMFF94",
    "protonation": "set_pH",
    "min_ph": 6.4,
    "max_ph": 8.4,
    "disconnect_group": true,
    "keep_large_fragment": true,
    "isomer_limit": 5,
    "tautomers": true,
    "stereoisomers": "general_all",
    "is_isomer": true
  },
  "docking": {
    "center": ["24.702", "-10.003", "-13.378"],
    "size": [28.217, 18.051, 23.973],
    "site": "A:KY9",
    "radius": 20.5957,
    "distance": 4.5,
    "scoring_function": "carsidock",
    "num_poses": 1,
    "flexible": "semi",
    "rescoring_functions": ["RTMS"]
  },
  "account": "person"
}
```

## Common Errors
1. `no pdb file provided`: missing `pdb` form field.
2. `no ligands file provided`: missing `ligands` form field.
3. `no ligands found in ligands file`: wrong ligands dataset or invalid smiles column.
4. `Insufficient account balance`: token/balance check failed.
5. `ws_id must be provided` or 404 on job list/detail: missing `ws_id` in request.
