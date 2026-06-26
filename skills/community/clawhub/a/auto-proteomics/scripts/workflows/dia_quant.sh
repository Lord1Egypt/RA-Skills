#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}

INPUT_TABLE=""
SAMPLE_SHEET=""
OUTPUT_DIR=""
INPUT_FORMAT="header-sample-matrix-v1"
NORMALIZED_INPUT_FORMAT=""
QUANT_LEVEL="protein"
SAMPLE_ID_COLUMN="sample_id"
GROUP_COLUMN="condition"
FEATURE_ID_COLUMN="feature_id"
DELIMITER="auto"
ALLOW_PARTIAL_MATCH="false"

usage() {
  cat <<'EOF'
Usage:
  dia_quant.sh --input-table <file> --sample-sheet <file> --output-dir <dir> [options]

Purpose:
  Prototype DIA processed-table intake workflow. This script validates one explicit
  first contract family, extracts a basic sample-aligned quant matrix, and writes
  lightweight QC artifacts plus a conservative post-filter normalization preview.
  It does not perform scientific DIA normalization or differential statistics.

Required:
  --input-table <file>              DIA quant table exported from an upstream tool
  --sample-sheet <file>             Sample annotation table with one row per sample
  --output-dir <dir>                Output directory for the prototype run bundle

Options:
  --input-format <name>             header-sample-matrix-v1 (default) or legacy alias generic-tsv
  --quant-level <name>              protein | peptide | precursor (default: protein)
  --sample-id-column <name>         Sample sheet column containing sample IDs (default: sample_id)
  --group-column <name>             Sample sheet column containing conditions/groups (default: condition)
  --feature-id-column <name>        Preferred feature identifier column in input table (default: feature_id)
  --delimiter <name>                auto | tab | comma (default: auto)
  --allow-partial-match             Keep run alive when some samples are unmatched
  -h, --help                        Show this help message

Minimal example:
  bash scripts/workflows/dia_quant.sh \
    --input-table data/dia_quant.tsv \
    --sample-sheet data/samples.tsv \
    --output-dir runs/dia_demo
EOF
}

write_contract_error() {
  local code=$1
  local message=$2
  local report_path=${3:-}
  if [[ -z "$report_path" ]]; then
    return 0
  fi
  mkdir -p "$(dirname "$report_path")"
  cat > "$report_path" <<EOF
{
  "workflow": "dia-quant",
  "mode": "prototype-technical-minimum",
  "status": "prototype",
  "support_level": "internal-prototype",
  "public_support": "not-shipped",
  "contract_family": "header-sample-matrix-v1",
  "contract_version": "1.0",
  "declared_input_format": "$INPUT_FORMAT",
  "normalized_input_format": "${NORMALIZED_INPUT_FORMAT:-}",
  "validation_status": "failed",
  "validation_errors": [
    {
      "code": "$code",
      "message": "$message"
    }
  ]
}
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input-table) INPUT_TABLE=$2; shift 2 ;;
    --sample-sheet) SAMPLE_SHEET=$2; shift 2 ;;
    --output-dir) OUTPUT_DIR=$2; shift 2 ;;
    --input-format) INPUT_FORMAT=$2; shift 2 ;;
    --quant-level) QUANT_LEVEL=$2; shift 2 ;;
    --sample-id-column) SAMPLE_ID_COLUMN=$2; shift 2 ;;
    --group-column) GROUP_COLUMN=$2; shift 2 ;;
    --feature-id-column) FEATURE_ID_COLUMN=$2; shift 2 ;;
    --delimiter) DELIMITER=$2; shift 2 ;;
    --allow-partial-match) ALLOW_PARTIAL_MATCH=true; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$INPUT_TABLE" || -z "$SAMPLE_SHEET" || -z "$OUTPUT_DIR" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

mkdir -p "$OUTPUT_DIR"/{logs,contract,matrix,qc,report,staging}
CONTRACT_REPORT_JSON="$OUTPUT_DIR/contract/validation_report.json"

if [[ ! -f "$INPUT_TABLE" ]]; then
  write_contract_error "input-table-not-found" "Input table not found: $INPUT_TABLE" "$CONTRACT_REPORT_JSON"
  echo "Input table not found: $INPUT_TABLE" >&2
  exit 1
fi
if [[ ! -f "$SAMPLE_SHEET" ]]; then
  write_contract_error "sample-sheet-not-found" "Sample sheet not found: $SAMPLE_SHEET" "$CONTRACT_REPORT_JSON"
  echo "Sample sheet not found: $SAMPLE_SHEET" >&2
  exit 1
fi

case "$INPUT_FORMAT" in
  header-sample-matrix-v1)
    NORMALIZED_INPUT_FORMAT="header-sample-matrix-v1"
    ;;
  generic-tsv)
    NORMALIZED_INPUT_FORMAT="header-sample-matrix-v1"
    ;;
  *)
    write_contract_error "unsupported-input-format" "Unsupported --input-format: $INPUT_FORMAT. DIA prototype currently validates only header-sample-matrix-v1 (legacy alias: generic-tsv)." "$CONTRACT_REPORT_JSON"
    echo "Unsupported --input-format: $INPUT_FORMAT" >&2
    exit 1
    ;;
esac

case "$QUANT_LEVEL" in
  protein|peptide|precursor) ;;
  *)
    write_contract_error "unsupported-quant-level" "Unsupported --quant-level: $QUANT_LEVEL" "$CONTRACT_REPORT_JSON"
    echo "Unsupported --quant-level: $QUANT_LEVEL" >&2
    exit 1
    ;;
esac

case "$DELIMITER" in
  auto|tab|comma) ;;
  *)
    write_contract_error "unsupported-delimiter" "Unsupported --delimiter: $DELIMITER" "$CONTRACT_REPORT_JSON"
    echo "Unsupported --delimiter: $DELIMITER" >&2
    exit 1
    ;;
esac

LOG_FILE="$OUTPUT_DIR/logs/workflow.log"
exec > >(tee "$LOG_FILE") 2>&1

INPUT_TABLE=$(cd "$(dirname "$INPUT_TABLE")" && pwd)/$(basename "$INPUT_TABLE")
SAMPLE_SHEET=$(cd "$(dirname "$SAMPLE_SHEET")" && pwd)/$(basename "$SAMPLE_SHEET")
OUTPUT_DIR=$(mkdir -p "$OUTPUT_DIR" && cd "$OUTPUT_DIR" && pwd)
CONTRACT_REPORT_JSON="$OUTPUT_DIR/contract/validation_report.json"

INPUT_SUMMARY_JSON="$OUTPUT_DIR/contract/input_summary.json"
MATCH_TABLE="$OUTPUT_DIR/contract/sample_column_mapping.tsv"
FORMAT_DIAGNOSTICS_JSON="$OUTPUT_DIR/contract/format_diagnostics.json"
CHECKED_METADATA="$OUTPUT_DIR/qc/sample_annotation.checked.tsv"
DETECTED_COLUMNS="$OUTPUT_DIR/matrix/detected_quant_columns.tsv"
QUANT_MATRIX="$OUTPUT_DIR/matrix/prototype_quant_preview.tsv"
SAMPLE_QC_TSV="$OUTPUT_DIR/qc/sample_quant_qc.tsv"
FEATURE_QC_TSV="$OUTPUT_DIR/qc/feature_quant_qc.tsv"
FILTERED_PREVIEW_TSV="$OUTPUT_DIR/matrix/prototype_filtered_preview.tsv"
FILTERING_REPORT_TSV="$OUTPUT_DIR/qc/feature_filtering_report.tsv"
NORMALIZED_PREVIEW_TSV="$OUTPUT_DIR/matrix/prototype_normalized_preview.tsv"
LOG2_NORMALIZED_PREVIEW_TSV="$OUTPUT_DIR/matrix/prototype_log2_normalized_preview.tsv"
NORMALIZATION_SUMMARY_JSON="$OUTPUT_DIR/qc/normalization_summary.json"
NORMALIZATION_QC_TSV="$OUTPUT_DIR/qc/normalization_diagnostics.tsv"
QC_SUMMARY_JSON="$OUTPUT_DIR/qc/summary.json"
REPORT_MD="$OUTPUT_DIR/report/REPORT.md"
NEXT_ACTIONS_MD="$OUTPUT_DIR/report/TODO_NEXT_ACTIONS.md"
MANIFEST_JSON="$OUTPUT_DIR/run_manifest.json"

"$PYTHON_BIN" "$ROOT_DIR/scripts/dia/build_matrix_and_qc.py" \
  --input-table "$INPUT_TABLE" \
  --sample-sheet "$SAMPLE_SHEET" \
  --sample-id-column "$SAMPLE_ID_COLUMN" \
  --group-column "$GROUP_COLUMN" \
  --feature-id-column "$FEATURE_ID_COLUMN" \
  --delimiter "$DELIMITER" \
  --output-matrix "$QUANT_MATRIX" \
  --output-filtered-matrix "$FILTERED_PREVIEW_TSV" \
  --output-sample-metadata "$CHECKED_METADATA" \
  --output-detected-columns "$DETECTED_COLUMNS" \
  --output-sample-qc "$SAMPLE_QC_TSV" \
  --output-feature-qc "$FEATURE_QC_TSV" \
  --output-filtering-report "$FILTERING_REPORT_TSV" \
  --output-qc-summary "$QC_SUMMARY_JSON" \
  --output-normalized-matrix "$NORMALIZED_PREVIEW_TSV" \
  --output-log-normalized-matrix "$LOG2_NORMALIZED_PREVIEW_TSV" \
  --output-normalization-summary "$NORMALIZATION_SUMMARY_JSON" \
  --output-normalization-qc "$NORMALIZATION_QC_TSV" \
  --output-input-summary "$INPUT_SUMMARY_JSON" \
  --output-format-diagnostics "$FORMAT_DIAGNOSTICS_JSON" \
  --output-contract-report "$CONTRACT_REPORT_JSON" \
  --input-format "$NORMALIZED_INPUT_FORMAT" \
  --declared-input-format "$INPUT_FORMAT" \
  --quant-level "$QUANT_LEVEL" \
  $( [[ "$ALLOW_PARTIAL_MATCH" == "true" ]] && printf '%s' '--allow-partial-match' )

"$PYTHON_BIN" - <<'PY' "$MATCH_TABLE" "$CHECKED_METADATA" "$SAMPLE_ID_COLUMN"
import csv
import sys
from pathlib import Path

match_table, checked_metadata, sample_id_column = sys.argv[1:]
with Path(checked_metadata).open("r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    rows = list(reader)

with Path(match_table).open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["sample_id", "input_column", "match_type"])
    for row in rows:
        sample_id = (row.get(sample_id_column) or "").strip()
        status = (row.get("column_match_status") or "missing").strip()
        input_column = sample_id if status != "missing" else ""
        writer.writerow([sample_id, input_column, status])
PY

cat > "$REPORT_MD" <<EOF
# DIA Quant Prototype Report

## Status

- workflow id: dia-quant
- execution mode: prototype-technical-minimum
- public support level: not shipped in v0.x
- scientific implementation: partial prototype only
- validated contract family: header-sample-matrix-v1

## What this run did

- validated one explicit DIA intake contract family rather than a generic processed table
- checked that the sample sheet contains $SAMPLE_ID_COLUMN and $GROUP_COLUMN
- performed exact matching between sample IDs and quant table headers
- wrote a sample-aligned quant matrix using the matched columns
- generated machine-readable contract metadata in contract/validation_report.json
- generated family-aware export diagnostics in contract/format_diagnostics.json
- generated basic per-sample QC summaries from the extracted matrix
- generated descriptive feature-level missingness and intensity summaries
- applied a prototype missingness-based filtering rule and wrote a filtered preview
- generated a conservative post-filter median-scaling normalization preview and summary
- derived a log2-transformed normalized preview strictly for internal prototype inspection
- generated minimal normalization diagnostics focused on sample-median alignment

## Produced files

- contract/validation_report.json
- contract/input_summary.json
- contract/sample_column_mapping.tsv
- contract/format_diagnostics.json
- qc/sample_annotation.checked.tsv
- qc/sample_quant_qc.tsv
- qc/feature_quant_qc.tsv
- qc/feature_filtering_report.tsv
- qc/normalization_summary.json
- qc/normalization_diagnostics.tsv
- qc/summary.json
- matrix/detected_quant_columns.tsv
- matrix/prototype_quant_preview.tsv
- matrix/prototype_filtered_preview.tsv
- matrix/prototype_normalized_preview.tsv
- matrix/prototype_log2_normalized_preview.tsv
- report/TODO_NEXT_ACTIONS.md

## Not implemented here

- software-specific DIA-NN or OpenMS export parsing beyond the current family-aware structural checks
- DIA-NN or OpenMS result normalization logic beyond the preview-only median scaling and log2 preview steps
- normalization QC beyond sample-median alignment diagnostics
- missing-value imputation or modeled missingness analysis
- scientific finality for the prototype filtering rule
- differential abundance statistics
- publication-ready biological interpretation
EOF

cat > "$NEXT_ACTIONS_MD" <<EOF
# Next Actions For DIA Prototype

1. Keep new demo and internal test runs pinned to the explicit contract family: header-sample-matrix-v1.
2. Review contract/validation_report.json first whenever intake fails.
3. Review contract/format_diagnostics.json to confirm that the export still fits the current family assumptions.
4. Review contract/sample_column_mapping.tsv and fix any missing sample-to-column matches.
5. Decide whether the next contract family should be truly software-specific or remain a second explicit wide-table family.
5. Decide whether the preview-only median scaling plus log2 preview steps should survive as a documented internal fallback.
6. Decide whether sample-median alignment diagnostics are enough or need replacement by format-aware normalization QC.
7. Add downstream statistics only after the parser and normalization contract are stable.

This file is intentionally operational, not scientific validation.
EOF

cat > "$MANIFEST_JSON" <<EOF
{
  "workflow": "dia-quant",
  "mode": "prototype-technical-minimum",
  "status": "prototype",
  "support_level": "internal-prototype",
  "public_support": "not-shipped",
  "contract_family": "header-sample-matrix-v1",
  "contract_version": "1.0",
  "declared_input_format": "$INPUT_FORMAT",
  "normalized_input_format": "$NORMALIZED_INPUT_FORMAT",
  "qc_scope": "structural-intake-plus-basic-numeric-summary-with-family-aware-export-diagnostics-feature-missingness-prototype-filtering-and-sample-median-normalization-diagnostics",
  "qc_limitations": [
    "not scientific DIA QC",
    "format-aware diagnostics are structural only",
    "validated only for the first explicit contract family",
    "feature missingness is descriptive only",
    "filtering is a prototype rule report, not a final scientific decision",
    "normalization is preview-only median scaling plus log2 preview after filtering",
    "normalization QC is limited to sample-median alignment diagnostics",
    "no missingness modeling or imputation",
    "no replicate CV analysis",
    "no instrument or software specific QC dashboard",
    "no differential statistics"
  ],
  "inputs": {
    "input_table": "$INPUT_TABLE",
    "sample_sheet": "$SAMPLE_SHEET",
    "input_format": "$INPUT_FORMAT",
    "normalized_input_format": "$NORMALIZED_INPUT_FORMAT",
    "quant_level": "$QUANT_LEVEL",
    "sample_id_column": "$SAMPLE_ID_COLUMN",
    "group_column": "$GROUP_COLUMN",
    "feature_id_column": "$FEATURE_ID_COLUMN",
    "allow_partial_match": $ALLOW_PARTIAL_MATCH
  },
  "outputs": {
    "contract_validation": "$CONTRACT_REPORT_JSON",
    "input_summary": "$INPUT_SUMMARY_JSON",
    "sample_mapping": "$MATCH_TABLE",
    "format_diagnostics": "$FORMAT_DIAGNOSTICS_JSON",
    "checked_metadata": "$CHECKED_METADATA",
    "detected_columns": "$DETECTED_COLUMNS",
    "prototype_quant_preview": "$QUANT_MATRIX",
    "prototype_filtered_preview": "$FILTERED_PREVIEW_TSV",
    "sample_qc": "$SAMPLE_QC_TSV",
    "feature_qc": "$FEATURE_QC_TSV",
    "filtering_report": "$FILTERING_REPORT_TSV",
    "prototype_normalized_preview": "$NORMALIZED_PREVIEW_TSV",
    "prototype_log2_normalized_preview": "$LOG2_NORMALIZED_PREVIEW_TSV",
    "normalization_qc": "$NORMALIZATION_QC_TSV",
    "normalization_summary": "$NORMALIZATION_SUMMARY_JSON",
    "qc_summary": "$QC_SUMMARY_JSON",
    "report": "$REPORT_MD",
    "next_actions": "$NEXT_ACTIONS_MD"
  }
}
EOF

echo "[auto-proteomics] DIA quant minimal technical prototype generated"
echo "status=prototype public_support=not-shipped contract_family=header-sample-matrix-v1"
echo "input_table=$INPUT_TABLE"
echo "sample_sheet=$SAMPLE_SHEET"
echo "output_dir=$OUTPUT_DIR"
echo "contract_validation=$CONTRACT_REPORT_JSON"
echo "report=$REPORT_MD"
