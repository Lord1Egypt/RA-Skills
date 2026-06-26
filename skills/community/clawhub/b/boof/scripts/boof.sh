#!/usr/bin/env bash
# boof.sh — Convert a PDF/document to markdown and index it for RAG retrieval
# Usage: boof.sh <input_file> [--collection <name>] [--output-dir <dir>]
#
# Requirements:
#   - Java 11+ (brew install openjdk or https://adoptium.net)
#   - opendataloader-pdf Python package (pip install opendataloader-pdf)
#     Install into a venv at $ODL_ENV or ~/.openclaw/tools/odl-env
#   - qmd (installed via: bun install -g https://github.com/tobi/qmd)
#
# What it does:
#   1. Converts PDF → markdown using opendataloader-pdf (local, no API calls)
#   2. Indexes the markdown into QMD for RAG retrieval
#   3. Outputs the path to the converted markdown file

set -euo pipefail

# --- Config ---
ODL_ENV="${ODL_ENV:-$HOME/.openclaw/tools/odl-env}"
QMD_BIN="${QMD_BIN:-$(command -v qmd 2>/dev/null || echo "$HOME/.bun/bin/qmd")}"
DEFAULT_OUTPUT_DIR="${BOOF_OUTPUT_DIR:-$HOME/.openclaw/workspace/knowledge/boofed}"

# Ensure Java is on PATH (Homebrew keg-only install)
if ! command -v java &>/dev/null; then
  for jpath in /opt/homebrew/opt/openjdk/bin /usr/local/opt/openjdk/bin; do
    if [[ -x "$jpath/java" ]]; then
      export PATH="$jpath:$PATH"
      break
    fi
  done
fi

# --- Parse args ---
INPUT_FILE=""
COLLECTION=""
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --collection) COLLECTION="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: boof.sh <input_file> [--collection <name>] [--output-dir <dir>]"
      echo ""
      echo "Convert a PDF to markdown and index it for RAG retrieval."
      echo ""
      echo "Options:"
      echo "  --collection <name>   QMD collection name (default: derived from filename)"
      echo "  --output-dir <dir>    Output directory (default: $DEFAULT_OUTPUT_DIR)"
      echo ""
      echo "Environment variables:"
      echo "  ODL_ENV               Path to opendataloader-pdf venv (default: ~/.openclaw/tools/odl-env)"
      echo "  QMD_BIN               Path to qmd binary (default: ~/.bun/bin/qmd)"
      echo "  BOOF_OUTPUT_DIR       Default output directory"
      exit 0
      ;;
    *) INPUT_FILE="$1"; shift ;;
  esac
done

if [[ -z "$INPUT_FILE" ]]; then
  echo "Error: No input file specified." >&2
  echo "Usage: boof.sh <input_file> [--collection <name>] [--output-dir <dir>]" >&2
  exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Error: File not found: $INPUT_FILE" >&2
  exit 1
fi

# --- Validate dependencies ---
ODL_PYTHON="$ODL_ENV/bin/python3"
if [[ ! -f "$ODL_PYTHON" ]]; then
  echo "Error: opendataloader-pdf venv not found at $ODL_ENV" >&2
  echo "Install:" >&2
  echo "  python3 -m venv $ODL_ENV" >&2
  echo "  $ODL_ENV/bin/pip install -U opendataloader-pdf" >&2
  exit 1
fi

# Verify opendataloader-pdf is installed in the venv
if ! "$ODL_PYTHON" -c "import opendataloader_pdf" 2>/dev/null; then
  echo "Error: opendataloader-pdf not installed in $ODL_ENV" >&2
  echo "Install: $ODL_ENV/bin/pip install -U opendataloader-pdf" >&2
  exit 1
fi

# Verify Java
if ! command -v java &>/dev/null; then
  echo "Error: Java not found. Install Java 11+:" >&2
  echo "  brew install openjdk" >&2
  echo "  # Then add to PATH: export PATH=\"/opt/homebrew/opt/openjdk/bin:\$PATH\"" >&2
  exit 1
fi

if [[ ! -x "$QMD_BIN" ]] && [[ ! -f "$QMD_BIN" ]]; then
  echo "Error: qmd not found at $QMD_BIN" >&2
  echo "Install: bun install -g https://github.com/tobi/qmd" >&2
  exit 1
fi

# --- Derive names ---
BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')
SAFE_NAME=$(echo "$BASENAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
COLLECTION="${COLLECTION:-$SAFE_NAME}"

# --- Step 1: Convert to markdown ---
echo "🍑 Boofing: $INPUT_FILE"
echo "   → Converting to markdown (opendataloader-pdf)..."
mkdir -p "$OUTPUT_DIR"

"$ODL_PYTHON" - 2>&1 <<PYEOF | grep -v "^Mar\|^INFO\|^WARNING" | sed 's/^/   /' || true
import opendataloader_pdf
opendataloader_pdf.convert(
    input_path=["$INPUT_FILE"],
    output_dir="$OUTPUT_DIR/",
    format="markdown"
)
PYEOF

# Find the output markdown file (ODL names it <basename>.md)
MD_FILE="$OUTPUT_DIR/${BASENAME}.md"

if [[ ! -f "$MD_FILE" ]]; then
  # Fallback: find most recently created .md in output dir
  MD_FILE=$(find "$OUTPUT_DIR" -name "*.md" -newer "$INPUT_FILE" 2>/dev/null | head -1)
fi

if [[ -z "$MD_FILE" ]] || [[ ! -f "$MD_FILE" ]]; then
  echo "Error: Could not find converted markdown file in $OUTPUT_DIR" >&2
  exit 1
fi

echo "   ✅ Markdown: $MD_FILE"

# --- Step 2: Index with QMD ---
echo "   → Indexing for RAG retrieval..."

if "$QMD_BIN" collection add "$(dirname "$MD_FILE")" --name "$COLLECTION" --mask "*.md" 2>&1 | sed 's/^/   /'; then
  echo "   → Building embeddings..."
  "$QMD_BIN" embed 2>&1 | tail -3 | sed 's/^/   /'
  echo "   ✅ Indexed as collection: $COLLECTION"
else
  echo "   ⚠️  QMD indexing failed (non-fatal). Markdown file still available." >&2
fi

# --- Done ---
echo ""
echo "🍑 Boofed successfully!"
echo "   Markdown: $MD_FILE"
echo "   Collection: $COLLECTION"
echo ""
echo "Query with:"
echo "   qmd query 'your question here' -c $COLLECTION"
