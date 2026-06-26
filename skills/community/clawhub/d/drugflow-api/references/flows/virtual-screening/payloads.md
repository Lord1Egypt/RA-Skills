# Virtual Screening Payload Notes

## Required Top-Level Keys (`args` JSON)
1. `input_type`
2. `input_source`
3. `steps`

Current implementation also relies on:
1. `protein` when step type is not `admet`
2. A 3-step sequence where index 1 is `karmadock` and index 2 is `carsidock`

## Supported Step Types
1. `admet`
2. `karmadock`
3. `carsidock`
4. `autodock_vina`
5. `autodock_rtms`

For this workflow, use:
1. `step1: admet`
2. `step2: karmadock`
3. `step3: carsidock`

---

## Protein / Pocket Parameters Explained

These parameters define **where on the protein the docking will be performed** (the binding pocket).

### `site`
- **Format**: `<chain>:<ligand_name>`, e.g. `"A:KY9"`
- **Meaning**: Identifies the binding site by the co-crystallised ligand. `A` is the chain ID, `KY9` is the 3-letter residue name of the reference ligand.
- **How to determine**: Parse the PDB file HETATM records, find the ligand of interest (typically the largest non-water, non-ion ligand), and combine its chain ID and residue name.

### `site_label`
- **Format**: `<chain>:<ligand_name>:<residue_id>`, e.g. `"A:KY9:601"`
- **Meaning**: Fully qualified label including the residue sequence number to disambiguate when the same ligand name appears at multiple positions.
- **How to determine**: Same as `site` but append the PDB residue sequence number (columns 23-27 of the HETATM line).

### `center`
- **Format**: `["x", "y", "z"]` (array of **string** floats, in Angstroms)
- **Meaning**: The geometric center of the docking box. Docking algorithms search for ligand poses within a box centered at this point.
- **How to determine**: Calculate the centroid of the reference ligand's atoms:
  ```
  center_x = (max_x + min_x) / 2
  center_y = (max_y + min_y) / 2
  center_z = (max_z + min_z) / 2
  ```

### `size`
- **Format**: `[x, y, z]` (array of floats, in Angstroms)
- **Meaning**: Dimensions of the docking search box along each axis. A larger box covers more space but is slower.
- **How to determine**: Compute the bounding box of the reference ligand and add padding (typically 10 Å per side):
  ```
  size_x = (max_x - min_x) + expand
  size_y = (max_y - min_y) + expand
  size_z = (max_z - min_z) + expand
  ```
  The default `expand = 10 Å` ensures the search box extends well beyond the ligand.

### `radius`
- **Format**: float (Angstroms)
- **Meaning**: Spherical search radius from the center, used by some scoring functions (e.g. CARSIDock) as an alternative/supplement to the box.
- **How to determine**: Maximum distance from any ligand atom to the center, plus half of the expand padding:
  ```
  radius = max_distance(atom, center) + expand / 2
  ```

### Automatic Detection from PDB File

When a local PDB file is available, the script `run_vs_flow.py` can **auto-detect** all pocket parameters by:
1. Parsing all HETATM records (excluding water `HOH` and common ions).
2. Grouping atoms by `(chain, residue_name, residue_id)`.
3. Selecting the ligand group with the **most atoms** (>= 6 atoms to exclude small fragments).
4. Computing `site`, `site_label`, `center`, `size`, `radius` from its bounding box.

Usage:
```bash
python3 scripts/virtual-screening/run_vs_flow.py \
  --base-url http://127.0.0.1:8888 \
  --email user@example.com --password secret \
  --protein-dataset-id DATASET_ID \
  --pdb-file /path/to/protein.pdb \
  --expand 10.0
```
When `--pdb-file` is given and `--site`/`--center`/`--size`/`--radius` are omitted, they are auto-filled.

You can also use the parser standalone:
```bash
python3 scripts/common/pdb_parser.py /path/to/protein.pdb --list-ligands
```

---

## Step-Level Parameters Explained

### ADMET Step (`step1`)
| Parameter | Description |
|-----------|-------------|
| `filter` | Array of ADMET property filters. Each entry has `name` and `rules`. |
| `filter[].name` | Property name: `MW` (molecular weight), `TPSA` (topological polar surface area), `LogS` (aqueous solubility), `LogP` (lipophilicity), `HBA` (H-bond acceptors), `HBD` (H-bond donors), etc. |
| `filter[].rules` | Array of conditions, e.g. `{"condition": "gt", "value": 300}`. Supported: `gt`, `lt`, `ge`, `le`, `eq`. |

Typical drug-like ranges (Lipinski's Rule of Five):
- MW: 150–500
- LogP: −0.4–5.6
- TPSA: 0–140
- LogS: −4–0.5

### KarmaDock Step (`step2`)
| Parameter | Description |
|-----------|-------------|
| `outpose` | Number of output poses per ligand (default `1`). |
| `filter.type` | `"top"` — keep top-N results. |
| `filter.order` | `"desc"` — higher score is better (KarmaDock returns positive scores). |
| `filter.expect.condition` | `"ge"` with a `value` — minimum count to keep. e.g. `50` keeps top-50. |

### CARSIDock Step (`step3`)
| Parameter | Description |
|-----------|-------------|
| `outpose` | Number of output poses per ligand (default `1`). |
| `isomers` | `false` — skip re-enumerating stereoisomers at this stage. |
| `filter` | Same format as KarmaDock. e.g. keep top-10 for final output. |

---

## Minimal Stable Template
```json
{
  "pdb": ["PROTEIN_DATASET_ID"],
  "pdb_name": "protein.pdb",
  "input_type": "db",
  "input_source": ["repurposing"],
  "input_source_labels": ["Drug Repurposing Compound Library(4317)"],
  "protein": {
    "protein_file": "PROTEIN_DATASET_ID",
    "site": "A:KY9",
    "site_label": "A:KY9:601",
    "center": ["24.702", "-10.003", "-13.378"],
    "size": [28.217, 18.051, 23.973],
    "radius": 20.5957
  },
  "steps": [
    {
      "id": 1,
      "type": "admet",
      "step": "step1",
      "args": {
        "filter": [
          {"name": "MW", "rules": [{"condition": "gt", "value": 300}, {"condition": "lt", "value": 400}]},
          {"name": "TPSA", "rules": [{"condition": "gt", "value": 0}, {"condition": "lt", "value": 140}]},
          {"name": "LogS", "rules": [{"condition": "gt", "value": -4}, {"condition": "lt", "value": 0.5}]},
          {"name": "LogP", "rules": [{"condition": "gt", "value": 1}, {"condition": "lt", "value": 3}]}
        ]
      }
    },
    {
      "id": 2,
      "type": "karmadock",
      "step": "step2",
      "args": {
        "outpose": 1,
        "filter": {"type": "top", "order": "desc", "expect": {"condition": "ge", "value": 50}}
      }
    },
    {
      "id": 3,
      "type": "carsidock",
      "step": "step3",
      "isomers": false,
      "args": {
        "outpose": 1,
        "filter": {"type": "top", "order": "desc", "expect": {"condition": "ge", "value": 10}}
      }
    }
  ],
  "account": "person"
}
```

## Other Top-Level Fields
| Field | Description |
|-------|-------------|
| `pdb` | Array containing the protein dataset ID (from dataset upload). |
| `pdb_name` | Display name for the protein file. |
| `input_type` | `"db"` (compound database) or `"file"` (user-uploaded file). |
| `input_source` | Array of database IDs, e.g. `["repurposing"]`. |
| `input_source_labels` | Human-readable labels for `input_source`. |
| `account` | `"person"` or `"team"` — determines which token pool to charge. |

## Common Errors and Fixes
1. `"ws_id must be provided."`: missing `ws_id` on `/api/jobs` create.
2. `404` on `/api/jobs` list/detail: missing `ws_id` query param.
3. `missing input_type/input_source/steps`: malformed `args` JSON.
4. `protein info is need in related steps`: non-`admet` step exists but no `protein` block.
5. Token-related create failure: refresh balance and estimate, then resubmit with valid `expect_tokens` and `avail_tokens`.
