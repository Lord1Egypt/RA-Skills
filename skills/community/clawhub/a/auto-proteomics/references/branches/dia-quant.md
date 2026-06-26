# DIA Quant Branch Spec

This document describes an internal prototype route kept inside a release-oriented repository.
It exists to make the future DIA branch legible and testable without promoting it as current public support.

- route id: `dia-quant`
- status: `prototype`
- visibility: `internal`
- public recommendation: `false`
- scientific goal: validate a minimal DIA processed-table contract and prepare a future quantification workflow without claiming public execution support
- route trigger: processed DIA result table + quantification goal
- route disambiguation: use this branch only for processed DIA tables that fit the checked-in DIA contract; raw DIA files belong to future upstream workflows, processed DDA tables belong to `dda-lfq-processed`, and generic downstream differential requests should stay out of `dia-quant`

## Expected upstream input family

This branch is for processed DIA result tables, not raw spectra.
For the current prototype, assume exactly one checked-in contract family: `header-sample-matrix-v1`.
That means a wide exported quant table whose sample IDs appear as column headers, plus a separate sample annotation table.

Do not describe this branch as supporting generic processed DIA tables beyond that explicit contract family.
Do not describe this branch as supporting software-specific DIA-NN or OpenMS parsing yet.

## Current implementation posture

The workflow entrypoint is now a prototype skeleton:
- it exposes a stable CLI
- it validates one explicit first contract family
- it emits machine-readable contract validation metadata and errors
- it writes a run bundle with explicit next-action files
- it still does not perform scientific DIA quantification

Public `v0.x` positioning remains unchanged: this route is not shipped.
Use it only for internal framework development or explicit prototype work.

## Required files

- DIA quantification table
- sample annotation table

For the exact first prototype schema, read `references/DIA_INPUT_SCHEMA.md`.

## Required sample-sheet fields

- `sample_id`
- `condition`

Both names are overridable in the CLI if a dataset uses different headers.

## Prototype-only command pattern

This command pattern documents the current prototype interface.
It is not a public support commitment and should not be surfaced as a shipped recommendation.

```bash
bash scripts/workflows/dia_quant.sh \
  --input-table <dia_quant.tsv> \
  --sample-sheet <samples.tsv> \
  --output-dir <output_dir> \
  --input-format header-sample-matrix-v1
```

## Fast route test

Ask these in order:
- is this proteomics data?
- is the acquisition mode DIA?
- is the input a processed table rather than raw files?
- is the user asking for quantification rather than differential downstream analysis?
- does the table fit `header-sample-matrix-v1` rather than some other DIA export family?

If any answer is no or unknown, do not select `dia-quant` yet.

## Current prototype outputs

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

Current QC content remains limited:
- `contract/validation_report.json` provides pass/fail intake state, contract family metadata, and machine-readable validation errors
- `qc/sample_quant_qc.tsv` provides sample-level completeness and simple intensity summaries only
- `qc/feature_quant_qc.tsv` provides descriptive feature-level missingness and simple intensity summaries only
- `qc/feature_filtering_report.tsv` provides a prototype keep/drop rule report only
- `qc/summary.json` records sample summaries plus top-level feature missingness, prototype filtering counts, and normalization-preview diagnostics
- `qc/normalization_summary.json` records preview-only median-scaling factors, per-sample post-scaling medians, and a compact sample-median alignment summary
- `qc/normalization_diagnostics.tsv` records per-sample pre/post median alignment against the prototype global median target
- `matrix/prototype_quant_preview.tsv` is the extracted feature-by-sample preview matrix before filtering
- `matrix/prototype_filtered_preview.tsv` is a filtered preview produced by the prototype missingness rule
- `matrix/prototype_normalized_preview.tsv` is a post-filter median-scaling preview only

## QC interpretation for small models

Treat the current QC layer as structural intake QC plus lightweight descriptive numeric summaries.
Expected QC-style outputs are limited to:
- contract-family validation and exact match policy
- sample-sheet validation with `column_match_status`
- exact sample-to-column mapping
- detected quant-column listing
- machine-readable matched/unmatched sample summary
- per-sample counts for detected, missing, and non-numeric feature cells
- per-feature counts for detected, missing, and non-numeric sample values

Do not imply that this branch already performs scientific DIA QC.
The current prototype does not produce scientifically final feature filtering decisions, validated normalization beyond sample-median alignment diagnostics, distribution plots, replicate CV summaries, or instrument/software-specific QC dashboards.

## Out-of-scope

- raw-spectrum DIA search from vendor files
- cross-software universal parsing in the first release
- normalization/statistics presented as scientifically complete
- implicit conversion from arbitrary peptide/site tables without explicit contract
- public `v0.x` execution claims

## Validation target

At minimum, this branch now validates:
- table readability and delimiter assumptions
- required sample-sheet columns
- exact sample-to-column mapping
- conformity to `header-sample-matrix-v1`
- sample-level completeness/intensity summaries from matched quant columns
- explicit prototype output generation
- machine-readable contract validation output

## Normalization boundary

Prototype normalization may be a reasonable next extension on top of the filtered preview, but it should be documented conservatively:
- keep any normalization outputs clearly separated from later statistics
- document normalization assumptions explicitly
- preserve the distinction between prototype preprocessing and final scientific interpretation
- do not claim normalization support unless the checked-in normalized preview artifacts and matching JSON/report boundary fields remain explicit about prototype scope

With those artifacts checked in, this branch may be described as supporting a normalization preview stage, but still not as full normalized DIA support or scientific normalization validation.

## Release-readiness checklist

- route wording is unambiguous
- route trigger and route disambiguation are explicit
- one clear input contract exists
- one clear execution file exists
- one small-model-readable command pattern exists
- outputs are explicit
- out-of-scope behavior is explicit
- public docs still describe this branch as not shipped
