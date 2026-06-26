# CP2K draft report

## Interpreted workflow
- Task type: {{ task_type }}
- Run type: {{ run_type }}
- System type: {{ system_type }}
- Structure file: {{ structure_file }}
- Periodicity: {{ periodicity }}
- Charge: {{ charge }}
- Multiplicity: {{ multiplicity }}
- Priority: {{ priority }}

## Method defaults
- XC functional: {{ xc_functional }}
- Basis family: {{ basis_family }}
- Potential family: {{ potential_family }}
- SCF mode: {{ scf_mode }}
- K-points: {{ kpoints_scheme }}
- Cell handling: {{ cell_handling }}

## Hardware
- Type: {{ hardware.type }}
- Cores: {{ hardware.cores }}
- Memory (GB): {{ hardware.memory_gb }}

## Defaults applied
{{ defaults_applied_block }}

## Notes and warnings
{{ notes_block }}

## Review required
{{ review_required_block }}

## Scope note
This file is a first-pass CP2K draft summary, not a convergence-validated production prescription.
