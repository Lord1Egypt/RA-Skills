# Demo Input Guide

## Goal

Prepare a generic processed-input demo or onboarding case for the first Auto-Proteomics release workflow: `dda-lfq-processed`.

This workflow does not start from raw spectra.
It expects processed protein-level quantification inputs that can be mapped into a MaxQuant-like layout.

## Required files

Place a reusable sample dataset under a dedicated demo directory, for example:

```text
examples/demo_processed_dda/
  proteinGroups.txt
  summary.txt
  parameters.txt
```

Required inputs:
- `proteinGroups.txt`
- `summary.txt`

Optional input:
- `parameters.txt`

## Minimal input contract

### `proteinGroups.txt`

Must be a tab-delimited table with:
- protein identifier columns such as `Protein IDs`
- quantitative columns matching either `LFQ intensity *` or `Intensity *`

Common metadata columns that are preserved when present:
- `Majority protein IDs`
- `Protein names`
- `Gene names`
- `Fasta headers`
- `Potential contaminant`
- `Reverse`
- `Only identified by site`

### `summary.txt`

Must be a tab-delimited table with at least:
- `Raw file`
- `Experiment`

The `Raw file` values must match the sample suffixes used in `proteinGroups.txt` quant columns.

Example:
- `LFQ intensity Sample_A_01` in `proteinGroups.txt`
- `Raw file = Sample_A_01` in `summary.txt`

### `parameters.txt`

Optional provenance file.
If available, keep the original processed-run parameters here.

## First release boundary

Current release boundary is intentionally narrow:
- processed DDA LFQ input only
- protein-level downstream analysis only
- one comparison: `group-a` vs `group-b`
- no raw search
- no peptide-level inference
- no enrichment in this first release validation

## Run command

For the bundled public demo, use the sample groups already present in `summary.txt`:
- `--group-a BoxCar`
- `--group-b Standard`

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

When reusing this pattern for another processed dataset, replace the group names with the exact `Experiment` values present in that dataset's `summary.txt`.

## Expected outputs

The workflow should generate:
- `results/REPORT.md`
- `results/summary.json`
- `results/run_manifest.json`
- `results/matrix/`
- `results/qc/`
- `results/stats/`

## Public-package rule

The public package may include lightweight demo inputs for smoke checks, but should not present demo or mock outputs as release validation evidence.

Release-readiness should be justified separately from `examples/` demo results.
If a real dataset is used for internal validation, keep that evidence outside the public demo story and do not center public entrypoints on a specific accession.
