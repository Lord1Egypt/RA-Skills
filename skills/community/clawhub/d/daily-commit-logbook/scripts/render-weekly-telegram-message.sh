#!/bin/bash
# Generate the weekly internship report and print a Telegram-ready summary message.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
export OPENCLAW_WORKSPACE="$WORKSPACE"

TMP_JSON=$(mktemp)
cleanup() {
    rm -f "$TMP_JSON"
}
trap cleanup EXIT

bash "$SCRIPT_DIR/generate-weekly-report.sh" > "$TMP_JSON"

TITLE=$(jq -r '.title' "$TMP_JSON")
START_LABEL=$(jq -r '.startLabel' "$TMP_JSON")
END_LABEL=$(jq -r '.endLabel' "$TMP_JSON")
SUMMARY=$(jq -r '.summary' "$TMP_JSON")
TEX_PATH=$(jq -r '.texPath' "$TMP_JSON")
PDF_PATH=$(jq -r '.pdfPath // empty' "$TMP_JSON")
NOTE=$(jq -r '.note' "$TMP_JSON")

PDF_LINE=""
if [ -n "$PDF_PATH" ] && [ "$PDF_PATH" != "null" ]; then
    PDF_LINE="- PDF: $PDF_PATH"
fi

cat <<EOF
📄 Weekly internship report ready.

Periode: $START_LABEL - $END_LABEL
Judul: $TITLE

Ringkasan:
$SUMMARY

Artefak:
$PDF_LINE
- LaTeX: $TEX_PATH

Catatan:
$NOTE
EOF
