#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}

INPUT_DIR=""
PROTEIN_GROUPS=""
SUMMARY_FILE=""
PARAMETERS_FILE=""
OUTPUT_DIR=""
GROUP_A=""
GROUP_B=""
MIN_VALID_VALUES=2
MISSINGNESS_THRESHOLD=0.7
PSEUDOCOUNT=1.0

usage() {
  cat <<'EOF'
Usage:
  dda_lfq_processed.sh --input-dir <dir> --protein-groups <file> --summary <file> \
    --output-dir <dir> --group-a <name> --group-b <name> [options]

Options:
  --parameters <file>               Optional MaxQuant parameters.txt
  --min-valid-values <n>            Minimum valid values in any group (default: 2)
  --missingness-threshold <float>   Max allowed overall missingness per protein (default: 0.7)
  --pseudocount <float>             Pseudocount before log2 transform (default: 1.0)
  -h, --help                        Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input-dir) INPUT_DIR=$2; shift 2 ;;
    --protein-groups) PROTEIN_GROUPS=$2; shift 2 ;;
    --summary) SUMMARY_FILE=$2; shift 2 ;;
    --parameters) PARAMETERS_FILE=$2; shift 2 ;;
    --output-dir) OUTPUT_DIR=$2; shift 2 ;;
    --group-a) GROUP_A=$2; shift 2 ;;
    --group-b) GROUP_B=$2; shift 2 ;;
    --min-valid-values) MIN_VALID_VALUES=$2; shift 2 ;;
    --missingness-threshold) MISSINGNESS_THRESHOLD=$2; shift 2 ;;
    --pseudocount) PSEUDOCOUNT=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$INPUT_DIR" || -z "$PROTEIN_GROUPS" || -z "$SUMMARY_FILE" || -z "$OUTPUT_DIR" || -z "$GROUP_A" || -z "$GROUP_B" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "Input directory not found: $INPUT_DIR" >&2
  exit 1
fi
if [[ ! -f "$PROTEIN_GROUPS" ]]; then
  echo "proteinGroups file not found: $PROTEIN_GROUPS" >&2
  exit 1
fi
if [[ ! -f "$SUMMARY_FILE" ]]; then
  echo "summary file not found: $SUMMARY_FILE" >&2
  exit 1
fi
if [[ -n "$PARAMETERS_FILE" && ! -f "$PARAMETERS_FILE" ]]; then
  echo "parameters file not found: $PARAMETERS_FILE" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"/{logs,intermediate,matrix,qc,stats}
LOG_FILE="$OUTPUT_DIR/logs/workflow.log"
exec > >(tee "$LOG_FILE") 2>&1

echo "[auto-proteomics] DDA LFQ processed workflow"
echo "input_dir=$INPUT_DIR"
echo "protein_groups=$PROTEIN_GROUPS"
echo "summary=$SUMMARY_FILE"
echo "group_a=$GROUP_A group_b=$GROUP_B"

STANDARDIZED="$OUTPUT_DIR/intermediate/protein_table.standardized.tsv"
RAW_MATRIX="$OUTPUT_DIR/matrix/protein_abundance_raw.tsv"
CHECKED_METADATA="$OUTPUT_DIR/matrix/sample_annotation.checked.tsv"
FILTERED_MATRIX="$OUTPUT_DIR/matrix/protein_abundance_filtered.tsv"
LOG2_MATRIX="$OUTPUT_DIR/matrix/protein_abundance_log2norm.tsv"
DIFF_ALL="$OUTPUT_DIR/stats/differential_proteins.tsv"
DIFF_SIG="$OUTPUT_DIR/stats/differential_proteins.sig.tsv"
REPORT_MD="$OUTPUT_DIR/REPORT.md"
SUMMARY_JSON="$OUTPUT_DIR/summary.json"
MANIFEST_JSON="$OUTPUT_DIR/run_manifest.json"

$PYTHON_BIN "$ROOT_DIR/scripts/dda/parse_processed_results.py" \
  --protein-groups "$PROTEIN_GROUPS" \
  --summary "$SUMMARY_FILE" \
  ${PARAMETERS_FILE:+--parameters "$PARAMETERS_FILE"} \
  --output "$STANDARDIZED"

$PYTHON_BIN "$ROOT_DIR/scripts/dda/build_protein_matrix.py" \
  --standardized "$STANDARDIZED" \
  --summary "$SUMMARY_FILE" \
  --output-matrix "$RAW_MATRIX" \
  --output-metadata "$CHECKED_METADATA"

$PYTHON_BIN "$ROOT_DIR/scripts/dda/qc_filter_normalize.py" \
  --matrix "$RAW_MATRIX" \
  --metadata "$CHECKED_METADATA" \
  --group-a "$GROUP_A" \
  --group-b "$GROUP_B" \
  --min-valid-values "$MIN_VALID_VALUES" \
  --missingness-threshold "$MISSINGNESS_THRESHOLD" \
  --pseudocount "$PSEUDOCOUNT" \
  --output-filtered "$FILTERED_MATRIX" \
  --output-log2norm "$LOG2_MATRIX" \
  --qc-dir "$OUTPUT_DIR/qc"

$PYTHON_BIN "$ROOT_DIR/scripts/dda/differential_protein.py" \
  --matrix "$LOG2_MATRIX" \
  --metadata "$CHECKED_METADATA" \
  --group-a "$GROUP_A" \
  --group-b "$GROUP_B" \
  --output-all "$DIFF_ALL" \
  --output-significant "$DIFF_SIG"

$PYTHON_BIN "$ROOT_DIR/scripts/dda/render_report.py" \
  --matrix "$LOG2_MATRIX" \
  --metadata "$CHECKED_METADATA" \
  --diff-all "$DIFF_ALL" \
  --diff-significant "$DIFF_SIG" \
  --report "$REPORT_MD" \
  --summary-json "$SUMMARY_JSON"

cat > "$MANIFEST_JSON" <<EOF
{
  "workflow": "dda-lfq-processed",
  "input_dir": "$INPUT_DIR",
  "protein_groups": "$PROTEIN_GROUPS",
  "summary": "$SUMMARY_FILE",
  "parameters": "${PARAMETERS_FILE:-}",
  "group_a": "$GROUP_A",
  "group_b": "$GROUP_B",
  "outputs": {
    "standardized": "$STANDARDIZED",
    "raw_matrix": "$RAW_MATRIX",
    "filtered_matrix": "$FILTERED_MATRIX",
    "log2_matrix": "$LOG2_MATRIX",
    "differential": "$DIFF_ALL",
    "report": "$REPORT_MD"
  }
}
EOF

echo "[auto-proteomics] Workflow completed"
