# Job spec schema

Normalize user requests into this contract before drafting the CP2K input.

```json
{
  "task_type": "geometry_optimization",
  "run_type": "GEO_OPT",
  "system_type": "molecule",
  "structure_file": "water.xyz",
  "structure_format": "xyz",
  "periodicity": "NONE",
  "charge": 0,
  "multiplicity": 1,
  "uks": false,
  "priority": "balanced",
  "xc_functional": "PBE",
  "basis_family": "DZVP-MOLOPT-SR-GTH",
  "potential_family": "GTH-PBE",
  "scf_mode": "OT",
  "kpoints_scheme": "GAMMA",
  "kpoints_grid": [1, 1, 1],
  "dispersion": false,
  "cell_handling": "auto_vacuum_box",
  "cell_vectors": null,
  "vacuum_padding_ang": 10.0,
  "cutoff": 500,
  "rel_cutoff": 60,
  "eps_scf": 1e-6,
  "max_scf": 100,
  "optimizer": "BFGS",
  "md": {
    "ensemble": null,
    "temperature_k": null,
    "timestep_fs": null,
    "steps": null
  },
  "hardware": {
    "type": "unknown",
    "cores": null,
    "memory_gb": null
  },
  "notes": [],
  "defaults_applied": [],
  "review_required": []
}
```

## Required top-level keys

- `task_type`
- `run_type`
- `system_type`
- `structure_file`
- `structure_format`
- `periodicity`
- `charge`
- `multiplicity`
- `uks`
- `priority`
- `xc_functional`
- `basis_family`
- `potential_family`
- `scf_mode`
- `kpoints_scheme`
- `kpoints_grid`
- `dispersion`
- `cell_handling`
- `cell_vectors`
- `vacuum_padding_ang`
- `cutoff`
- `rel_cutoff`
- `eps_scf`
- `max_scf`
- `optimizer`
- `md`
- `hardware`
- `notes`
- `defaults_applied`
- `review_required`

## Review-required examples

Populate `review_required` for cases such as:
- uncertain spin state
- periodic material inferred from `.xyz`
- heuristic k-point mesh
- transition-metal pseudopotential placeholder
- dispersion guessed from a vague adsorption request
- unsupported structure format during deterministic rendering
