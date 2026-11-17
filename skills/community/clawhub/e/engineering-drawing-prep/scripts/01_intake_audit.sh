#!/bin/bash
# 01_intake_audit.sh — Inventory, hash, and audit raw client deliverables.
# Usage: bash 01_intake_audit.sh <client_given_dir> [output_dir]

set -euo pipefail

SRC="${1:?Usage: $0 <client_given_dir> [output_dir]}"
OUT="${2:-./output}"
REPORT_DIR="$OUT/reports"
mkdir -p "$REPORT_DIR"

TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
MANIFEST="$REPORT_DIR/intake_manifest_$TIMESTAMP.jsonl"
HASH_LOG="$REPORT_DIR/sha256_hashes_$TIMESTAMP.txt"
NOISE_LOG="$REPORT_DIR/removed_noise_$TIMESTAMP.txt"

echo "=========================================="
echo " Intake Audit: $SRC"
echo " Output: $OUT"
echo "=========================================="

# 1. Clean macOS noise
echo "[1/4] Removing macOS noise files..."
find "$SRC" -type f \( -name '._*' -o -name '.DS_Store' -o -name '*.dwl' -o -name '*.dwl2' \) -print > "$NOISE_LOG" | while read -r f; do
    rm -f "$f"
done
echo "  Noise files removed: $(wc -l < "$NOISE_LOG" | tr -d ' ')"

# 2. Inventory and hash
echo "[2/4] Inventory and SHA-256..."
echo "# SHA-256 hashes generated at $TIMESTAMP" > "$HASH_LOG"
find "$SRC" -type f | sort | while read -r f; do
    rel="${f#$SRC/}"
    size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo "unknown")
    hash=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}' || sha256sum "$f" 2>/dev/null | awk '{print $1}' || echo "unsupported")
    ext="${f##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    mime="unknown"
    case "$ext_lower" in
        dwg) mime="application/acad" ;;
        dxf) mime="application/dxf" ;;
        pdf) mime="application/pdf" ;;
        xlsx|xls) mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ;;
        docx|doc) mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
        shx|ttf) mime="font" ;;
        *) mime="application/octet-stream" ;;
    esac
    printf '{"path":"%s","size":%s,"sha256":"%s","mime":"%s","timestamp":"%s"}\n' "$rel" "$size" "$hash" "$mime" "$TIMESTAMP" >> "$MANIFEST"
    printf '%s  %s\n' "$hash" "$rel" >> "$HASH_LOG"
done
echo "  Files inventoried: $(wc -l < "$MANIFEST" | tr -d ' ')"

# 3. Quick openability check for DWGs
echo "[3/4] DWG openability probe..."
DWG_CHECK="$REPORT_DIR/dwg_openability_$TIMESTAMP.txt"
echo "# DWG openability check at $TIMESTAMP" > "$DWG_CHECK"
find "$SRC" -type f -iname '*.dwg' | while read -r f; do
    rel="${f#$SRC/}"
    # Basic magic-number check: DWG files start with "AC10xx" or similar
    magic=$(head -c 6 "$f" | cat -v | head -c 20)
    if echo "$magic" | grep -qE 'AC10|AC10(11|15|18|21|24|27|32|10(21|24|27|32|36|40|44|48|52|56))'; then
        status="likely_valid"
    else
        status="CHECK_MAGIC"
    fi
    printf '%s\t%s\t%s\n' "$rel" "$status" "$magic" >> "$DWG_CHECK"
done
echo "  DWGs checked: $(grep -c '^' "$DWG_CHECK" || echo 0)"

# 4. Summary
echo "[4/4] Summary"
echo "  Manifest:      $MANIFEST"
echo "  Hashes:        $HASH_LOG"
echo "  Noise log:     $NOISE_LOG"
echo "  DWG check:     $DWG_CHECK"
echo "=========================================="
echo "Intake audit complete."
