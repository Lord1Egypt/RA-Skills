# Decision Target Map

This file defines the stable target names used by the AutoMD-GROMACS decision layer.

## Core Rule

Use `decision -> execution -> validation` as the product-facing stack.

Do not use folder names such as `advanced` or `analysis` as routing concepts.
Those are storage/layout details, not decision semantics.

## Layer Model

### Decision

Front-door routing before execution.

Canonical entrypoint:
- `method-selector`

### Execution

Run simulation, setup, or method workflows after routing.

Canonical target families:
- `execution-core`
- `execution-sampling`
- `execution-special`

### Validation

Interpret, quality-check, compare, and visualize results after execution.

Canonical target family:
- `validation-analysis`

## Canonical Execution Targets

### Core

- `workflow` -> `scripts/advanced/workflow.sh`
- `production` -> `scripts/basic/production.sh`
- `preprocess` -> `scripts/basic/preprocess.sh`
- `utils-tools` -> `scripts/basic/utils.sh`

### Sampling

- `replica-exchange` -> `scripts/advanced/replica-exchange.sh`
- `metadynamics` -> `scripts/advanced/metadynamics.sh`
- `steered-md` -> `scripts/advanced/steered-md.sh`
- `accelerated-md` -> `scripts/advanced/accelerated-md.sh`
- `enhanced-sampling` -> `scripts/advanced/enhanced-sampling.sh`
- `umbrella` -> `scripts/advanced/umbrella.sh`
- `freeenergy` -> `scripts/advanced/freeenergy.sh`

### Special

- `membrane` -> `scripts/advanced/membrane.sh`
- `electric-field` -> `scripts/advanced/electric-field.sh`
- `coarse-grained` -> `scripts/advanced/coarse-grained.sh`
- `non-equilibrium` -> `scripts/advanced/non-equilibrium.sh`
- `qmmm` -> `scripts/advanced/qmmm.sh`
- `protein-setup` -> `scripts/advanced/protein.sh`

## Canonical Validation Targets

- `trajectory-analysis` -> `scripts/analysis/trajectory-analysis.sh`
- `advanced-analysis` -> `scripts/analysis/advanced-analysis.sh`
- `binding-analysis` -> `scripts/analysis/binding-analysis.sh`
- `property-analysis` -> `scripts/analysis/property-analysis.sh`
- `membrane-analysis` -> `scripts/analysis/membrane-analysis.sh`
- `free-energy-analysis` -> `scripts/analysis/free-energy-analysis.sh`
- `protein-analysis` -> `scripts/advanced/protein.sh`
- `protein-special-analysis` -> `scripts/analysis/protein-special-analysis.sh`
- `scattering-analysis` -> `scripts/analysis/scattering-analysis.sh`
- `publication-viz` -> `scripts/visualization/publication-viz.sh`

## Naming Rules

- Use lower-case kebab-case target ids.
- Use method names for execution targets.
- Use task names for validation targets.
- Keep `freeenergy` and `free-energy-analysis` separate.
- Keep `protein-setup`, `protein-analysis`, and `protein-special-analysis` separate.
- Do not route with raw file paths as the primary label.
- Do not mix snake_case and kebab-case for the same public target.

## Important Boundaries

### `freeenergy` vs `free-energy-analysis`

- `freeenergy` = run alchemical/free-energy workflow
- `free-energy-analysis` = evaluate BAR/WHAM/AWH outputs after execution

### `protein-setup` vs `protein-analysis` vs `protein-special-analysis`

- `protein-setup` = execution helper under special workflows
- `protein-analysis` = standard post-analysis
- `protein-special-analysis` = mechanism-focused protein interpretation

### `publication-viz`

Treat as validation/output presentation, not execution.
It packages results for figures, reports, and publication-ready export.

## Recommended Decision Output Style

Use canonical target ids in `Recommended` and use script paths only in `Next`.

Example:

```text
Recommended: replica-exchange
Why: broad exploration needed and no credible CV is available
Avoid: metadynamics
Next: scripts/advanced/replica-exchange.sh
```
