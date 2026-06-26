# Runtime Requirements

## Public `v0.x` runtime target

This skill currently ships one supported runnable workflow:
- `scripts/workflows/dda_lfq_processed.sh`

All other workflow scripts in `scripts/workflows/` are future scaffold in `v0.x`.
They may help routing or future development, but they are not part of the public execution promise.

## Required tools

- `bash`
- `python3`
- Python package: `PyYAML` for the routing helper

Install the minimal Python dependency with:

```bash
python3 -m pip install PyYAML
```

## Processed-input assumptions

The shipped workflow expects processed protein-level DDA LFQ input, not raw instrument data.

Required files:
- `proteinGroups.txt`
- `summary.txt`

Optional file:
- `parameters.txt`

Expected columns:
- `proteinGroups.txt`: `LFQ intensity *` or `Intensity *`
- `summary.txt`: `Raw file` and `Experiment`

The `Raw file` values in `summary.txt` must match the sample suffixes used in the quantitative columns.

## Public promise vs future scaffold

Public promise now:
- route eligible requests into `dda-lfq-processed`
- parse MaxQuant-like processed protein tables
- build matrix, QC, differential, and report outputs for one two-group comparison

Future scaffold only:
- raw DDA identification
- DIA quantification
- phosphoproteomics workflows
- enrichment workflows
- multi-omics planning/execution

## Minimal verification

Check that the router recommends the shipped workflow:

```bash
python3 scripts/decision/route_proteomics.py \
  --data-type proteomics \
  --acquisition-mode dda \
  --target-output differential-analysis \
  --pretty
```

Expected recommendation:
- `dda-lfq-processed`

Check that the shipped workflow exposes its CLI contract:

```bash
bash scripts/workflows/dda_lfq_processed.sh --help
```

## Non-goals for this release

This public `v0.x` release does not claim:
- end-to-end raw-spectrum analysis
- universal compatibility with every processed proteomics export format
- automatic experimental design inference
- support for complex contrasts, batches, or multi-factor models
