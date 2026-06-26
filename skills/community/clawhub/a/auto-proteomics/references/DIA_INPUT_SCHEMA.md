# DIA Input Schema

## Goal

This document defines the first explicit processed-table contract family for the `dia-quant` prototype.

It is intentionally narrow.
The purpose is to give smaller models and human users one clear contract that is easy to validate and hard to misread.

## Current status

- branch: `dia-quant`
- status: `prototype`
- public support: not shipped in `v0.x`
- first contract family: `header-sample-matrix-v1`

This schema is for internal framework development and explicit prototype work.
It should not be described as public execution support yet.

## First supported input shape

The current prototype supports exactly one checked-in contract family:
- contract family: `header-sample-matrix-v1`
- one tabular DIA quantification file
- one tabular sample sheet
- sample IDs from the sample sheet must appear as quant table headers

This is the only schema the prototype should assume for now.
Do not imply broader universal DIA support.
Do not describe `dia-quant` as supporting DIA-NN, OpenMS, or generic processed DIA tables beyond this explicit contract family.

## Files

### 1. DIA quant table

Expected form:
- tab-delimited `.tsv` by default
- comma-delimited `.csv` also supported
- one feature identifier column
- one numeric quant column per sample

Current prototype assumption:
- sample IDs are stored directly in quant table column headers
- no long-format table support yet
- no automatic pivoting yet
- no software-specific parser behavior yet

### 2. Sample sheet

Expected form:
- tab-delimited `.tsv` by default
- comma-delimited `.csv` also supported
- one row per sample

Required columns by default:
- `sample_id`
- `condition`

These names can be changed with CLI options:
- `--sample-id-column`
- `--group-column`

## Minimal table rules

### DIA quant table

Must contain:
- at least one feature identifier column
- at least one sample quant column

Current feature ID detection order:
1. user-supplied `--feature-id-column`
2. `feature_id`
3. `Protein.Group`
4. `ProteinName`
5. `PG.ProteinGroups`
6. `Protein`
7. otherwise the first column

### Sample matching rule

Current strict rule:
- every `sample_id` in the sample sheet must appear exactly as a quant table header

If exact matching fails:
- default behavior: stop with an error
- machine-readable failure is written to `contract/validation_report.json`
- optional behavior: rerun with `--allow-partial-match` to generate a prototype contract bundle only

## Explicitly unsupported in the first schema

Not supported yet:
- raw DIA vendor files
- raw DIA search outputs
- multi-table assembly from several exports
- long-format intensity tables that need reshaping
- automatic synonym matching for sample IDs
- automatic normalization or statistical inference
- peptide/site-table auto-conversion without an explicit contract
- software-specific DIA-NN / OpenMS parser guarantees

## Small-model route test

A smaller model should only choose `dia-quant` when all of these are true:
- the data is proteomics
- the acquisition mode is DIA
- the input is already a processed table
- the user wants quantification intake rather than differential downstream analysis
- the sample sheet has stable sample IDs that match quant table headers
- the processed table fits `header-sample-matrix-v1`

If any of those are not clear, stop and ask instead of guessing.

## Prototype-only command

Run this only for explicit prototype evaluation or internal framework work.
Do not cite it as a public `v0.x` supported workflow command.

```bash
bash scripts/workflows/dia_quant.sh \
  --input-table <dia_quant.tsv> \
  --sample-sheet <samples.tsv> \
  --output-dir <output_dir> \
  --input-format header-sample-matrix-v1
```

Legacy note:
- `--input-format generic-tsv` is still accepted as a compatibility alias
- it is normalized to `header-sample-matrix-v1` in machine-readable metadata
- new docs and tests should use the explicit contract-family name

## Prototype outputs

Current prototype emits:
- `contract/validation_report.json`
- `contract/input_summary.json`
- `contract/sample_column_mapping.tsv`
- `qc/sample_annotation.checked.tsv`
- `qc/sample_quant_qc.tsv`
- `qc/feature_quant_qc.tsv`
- `qc/feature_filtering_report.tsv`
- `qc/summary.json`
- `qc/normalization_summary.json`
- `qc/normalization_diagnostics.tsv`
- `matrix/detected_quant_columns.tsv`
- `matrix/prototype_quant_preview.tsv`
- `matrix/prototype_filtered_preview.tsv`
- `matrix/prototype_normalized_preview.tsv`
- `matrix/prototype_log2_normalized_preview.tsv`
- `report/REPORT.md`
- `report/TODO_NEXT_ACTIONS.md`
- `run_manifest.json`
- `logs/workflow.log`

Important precision note:
- normalized preview outputs exist, but they remain prototype-only preprocessing previews
- they must not be described as scientific DIA normalization support

Current numeric QC content is still narrow:
- `qc/sample_quant_qc.tsv` contains per-sample counts and simple intensity summaries: `total_features`, `detected_features`, `missing_values`, `non_numeric_values`, `detection_rate`, `min_intensity`, `median_intensity`, `max_intensity`
- `qc/feature_quant_qc.tsv` contains per-feature descriptive summaries: `detected_samples`, `missing_values`, `non_numeric_values`, `missing_rate`, `min_intensity`, `mean_intensity`, `median_intensity`, `max_intensity`
- `qc/feature_filtering_report.tsv` contains a prototype keep/drop rule report based on a conservative missingness threshold
- `qc/summary.json` repeats sample-level summaries and adds top-level feature missingness summary fields such as `complete_features`, `partial_missing_features`, `fully_missing_features`, `missingness_rate_mean`, and `features_with_any_missing`
- `qc/normalization_summary.json` records the prototype median-scaling preview and derived log2 preview summary
- `contract/validation_report.json` records contract family, declared-vs-normalized input format, exact matching policy, and machine-readable validation errors when intake fails

Machine-readable boundary fields now included in JSON outputs:
- `support_level`
- `public_support`
- `contract_family`
- `contract_version`
- `qc_scope`
- `qc_limitations`

## QC contract for the minimal prototype

For the current technical prototype, QC means structural intake checks plus lightweight descriptive summaries.
A smaller model should expect these QC-style artifacts:
- `contract/validation_report.json`: contract family metadata plus pass/fail validation result
- `qc/sample_annotation.checked.tsv`: sample sheet copied forward with `column_match_status`
- `contract/sample_column_mapping.tsv`: explicit sample-to-header match table
- `contract/format_diagnostics.json`: prototype family-aware export-structure checks for the current first export family
- `matrix/detected_quant_columns.tsv`: detected feature/sample/unclassified columns
- `qc/sample_quant_qc.tsv`: per-sample completeness and basic numeric summaries
- `qc/feature_quant_qc.tsv`: per-feature missingness and basic numeric summaries
- `contract/input_summary.json`: machine-readable summary of matched and unmatched samples
- `qc/summary.json`: top-level summary of sample counts, feature missingness, prototype filtering counts, and normalization preview summaries

These files answer a narrow question:
- are the provided files readable?
- are required sample-sheet columns present?
- do sample IDs map to quant-table headers?
- does the input fit `header-sample-matrix-v1`?
- which columns are currently treated as quant columns?
- for each matched sample, how many feature cells are numeric vs missing or non-numeric?
- for each feature, how many samples are detected vs missing or non-numeric?

They still do not answer scientific QC questions about DIA signal quality.

## QC artifacts that are not expected yet

Do not expect the first prototype to emit any of the following:
- final scientific feature filtering decisions
- missingness modeling or imputation
- intensity distribution plots
- TIC/BPC style run-level summaries
- CV tables across replicates
- precursor/protein identification counts by run
- retention time, m/z, or interference diagnostics
- batch effect PCA/UMAP plots
- outlier detection reports
- software-specific DIA-NN / OpenMS QC dashboards

Important precision note:
- `qc/sample_quant_qc.tsv` already includes sample-level `missing_values` and `detection_rate`
- `qc/feature_quant_qc.tsv` adds feature-level descriptive missingness summaries
- `qc/feature_filtering_report.tsv` and `matrix/prototype_filtered_preview.tsv` document a prototype missingness rule, not a final scientific filtering decision
- `qc/normalization_summary.json` and the normalized matrix previews remain prototype-only preprocessing outputs
- these are descriptive prototype summaries, not a scientific missingness model, normalization validation, or filtering decision

If such QC is required, the correct interpretation is: this branch is still pre-scientific and needs a later implementation step.
