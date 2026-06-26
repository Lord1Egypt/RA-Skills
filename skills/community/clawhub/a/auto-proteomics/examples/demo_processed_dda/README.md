# Demo Processed DDA Input

This directory contains lightweight sample inputs for local smoke checks of `dda-lfq-processed`.
It is not a release-validation dataset, and generated outputs under `results/` should stay out of the public package.

## Demo groups

The bundled demo can be run directly with:
- `--group-a BoxCar`
- `--group-b Standard`

## Quick run

```bash
bash scripts/workflows/dda_lfq_processed.sh \
  --input-dir examples/demo_processed_dda \
  --protein-groups examples/demo_processed_dda/proteinGroups.txt \
  --summary examples/demo_processed_dda/summary.txt \
  --parameters examples/demo_processed_dda/parameters.txt \
  --output-dir examples/demo_processed_dda/results \
  --group-a BoxCar \
  --group-b Standard
```

If you are adapting this demo to your own processed input, replace only the file paths and group names while keeping the same input layout.
