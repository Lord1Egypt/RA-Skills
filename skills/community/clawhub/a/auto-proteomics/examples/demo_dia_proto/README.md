# Demo DIA Prototype Input

This directory contains a tiny prototype fixture for `dia-quant`.

Use it only for internal framework testing.
It does not mean DIA is publicly shipped in `v0.x`.

## Contract family

This demo is pinned to the first explicit DIA intake contract family:
- `header-sample-matrix-v1`

Interpretation:
- one wide processed DIA quant table
- one sample sheet
- sample IDs must match quant-table headers exactly

This is narrower than a generic processed DIA table claim.
It is the only checked-in DIA contract family the current prototype validates.

## QC expectation

This demo checks the minimal DIA intake contract plus lightweight prototype summaries.
Expected outputs are structural files such as `contract/validation_report.json`, `qc/sample_annotation.checked.tsv`, `contract/sample_column_mapping.tsv`, `matrix/detected_quant_columns.tsv`, and `contract/input_summary.json`, plus lightweight numeric summaries in `qc/sample_quant_qc.tsv`, `qc/feature_quant_qc.tsv`, `qc/feature_filtering_report.tsv`, `qc/normalization_summary.json`, `qc/normalization_diagnostics.tsv`, and `qc/summary.json`.

In this demo, `qc/sample_quant_qc.tsv` remains limited to per-sample counts and simple intensity summaries over the extracted feature-by-sample matrix. `qc/feature_quant_qc.tsv` adds descriptive per-feature missingness counts, missingness rates, and basic intensity summaries. `qc/feature_filtering_report.tsv` adds a conservative prototype keep/drop rule based on feature missingness. `qc/normalization_summary.json` records both the prototype median-scaling preview and a derived log2 preview summary. `qc/normalization_diagnostics.tsv` adds sample-median alignment diagnostics for the scaling preview only. `qc/summary.json` repeats the sample summaries and adds top-level feature missingness, prototype filtering, and normalization-preview counts. `contract/validation_report.json` records pass/fail intake state, contract family, and machine-readable validation errors.

The current checked-in matrix previews are precise and limited:
- `matrix/prototype_quant_preview.tsv` is the raw matched feature-by-sample preview
- `matrix/prototype_filtered_preview.tsv` is the preview after the prototype missingness rule
- `matrix/prototype_normalized_preview.tsv` is a post-filter preview-only median-scaling matrix for internal prototype evaluation
- `matrix/prototype_log2_normalized_preview.tsv` is a log2 transform of the positive normalized preview values for internal inspection only

Do not read this demo as scientific DIA QC, shipped normalized DIA support, or final scientific filtering.
It does not currently provide validated normalization, scientific log-transform handling, intensity distribution plots, replicate CV diagnostics, DIA-NN/OpenMS quality dashboards, or modeled missingness analysis.

## Quick run

```bash
bash scripts/workflows/dia_quant.sh \
  --input-table examples/demo_dia_proto/dia_quant.tsv \
  --sample-sheet examples/demo_dia_proto/samples.tsv \
  --output-dir examples/demo_dia_proto/results \
  --input-format header-sample-matrix-v1
```

Legacy note:
- `--input-format generic-tsv` still works as a compatibility alias
- new tests and documentation should use `header-sample-matrix-v1`
