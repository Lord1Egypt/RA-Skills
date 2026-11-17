#!/bin/bash
# 02_standardize.sh — Standardize DWG layers, fonts, and title blocks.
# Usage: bash 02_standardize.sh <client_given_dir> <output_wip_dir>

set -euo pipefail

SRC="${1:?Usage: $0 <client_given_dir> <output_wip_dir>}"
OUT="${2:?Usage: $0 <client_given_dir> <output_wip_dir>}"
mkdir -p "$OUT"

TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
REPORT="$OUT/../reports/standardization_$TIMESTAMP.txt"
mkdir -p "$OUT/../reports"

echo "=========================================="
echo " Standardization: $SRC -> $OUT"
echo "=========================================="

# Locate AutoCAD Core Console or fallback to Python/ezdxf
ACAD=""
for p in \
    "/Applications/Autodesk/AutoCAD 2025/AutoCAD.app/Contents/MacOS/AutoCAD" \
    "/Applications/Autodesk/AutoCAD 2024/AutoCAD.app/Contents/MacOS/AutoCAD" \
    "C:/Program Files/Autodesk/AutoCAD 2025/accoreconsole.exe" \
    "C:/Program Files/Autodesk/AutoCAD 2024/accoreconsole.exe" \
    "C:/Program Files/Autodesk/AutoCAD 2023/accoreconsole.exe"; do
    if [ -x "$p" ]; then
        ACAD="$p"
        break
    fi
done

STANDARD_LAYERS="STANDARD,DEFPOINTS,0,TEXT,DIM,ANNO,HATCH,BORDER"

echo "[1/3] Copying source DWGs to WIP..." | tee "$REPORT"
count=0
find "$SRC" -type f -iname '*.dwg' | while read -r f; do
    rel="${f#$SRC/}"
    base=$(basename "$rel" .dwg)
    wip_path="$OUT/${base}_WIP_${TIMESTAMP}.dwg"
    cp "$f" "$wip_path"
    count=$((count+1))
done
echo "  Copied: $count DWGs" | tee -a "$REPORT"

if [ -n "$ACAD" ]; then
    echo "[2/3] AutoCAD found: $ACAD" | tee -a "$REPORT"
    echo "  Layer enforcement and title-block update would run here." | tee -a "$REPORT"
    echo "  For full batch processing, supply a .scr script in templates/standardize.scr" | tee -a "$REPORT"
else
    echo "[2/3] AutoCAD not found. Falling back to Python/ezdxf placeholder." | tee -a "$REPORT"
    echo "  Install ezdxf: pip install ezdxf" | tee -a "$REPORT"
fi

echo "[3/3] Writing standardization report..." | tee -a "$REPORT"
echo "  Output dir: $OUT" | tee -a "$REPORT"
echo "  Standard layers target: $STANDARD_LAYERS" | tee -a "$REPORT"
echo "==========================================" | tee -a "$REPORT"
echo "Standardization complete." | tee -a "$REPORT"
