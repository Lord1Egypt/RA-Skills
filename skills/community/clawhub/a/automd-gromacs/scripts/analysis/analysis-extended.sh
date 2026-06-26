#!/bin/bash
# GROMACS Analysis Extensions (Python fallback for GROMACS 2026 bugs)
# Provides: MSD, residue distances, chi angles
# Uses MDAnalysis as fallback for broken gmx commands
set -e

SKILL_ROOT="${SKILL_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
PY_SCRIPTS="$SKILL_ROOT/scripts/analysis/py"

TPR="${TPR:-md.tpr}"
GRO="${GRO:-md.gro}"
TRJ="${TRJ:-md.trr}"
OUTPUT="${OUTPUT:-py_analysis}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
check_python_pkg() {
    python3 -c "import $1" 2>/dev/null && echo "  ✅ $1" || echo "  ❌ $1 (pip install $1)"
}

# Resolve absolute paths FIRST, before cd
TRJ_ABS=$(realpath "$TRJ" 2>/dev/null || readlink -f "$TRJ" 2>/dev/null || echo "$(pwd)/$TRJ")
GRO_ABS=$(realpath "$GRO" 2>/dev/null || readlink -f "$GRO" 2>/dev/null || echo "$(pwd)/$GRO")
TPR_ABS=$(realpath "$TPR" 2>/dev/null || readlink -f "$TPR" 2>/dev/null || echo "$(pwd)/$TPR")
NDX_ABS=$(realpath "${NDX:-analysis.ndx}" 2>/dev/null || echo "")

mkdir -p "$OUTPUT"
cd "$OUTPUT"

echo "=== Dependencies ==="
check_python_pkg MDAnalysis
check_python_pkg numpy
check_python_pkg tidynamics
echo ""

# --- MSD (Diffusion Coefficient) ---
if [ "${SKIP_MSD:-0}" != "1" ]; then
    log "=== MSD: Diffusion coefficient ==="
    [ -f "$GRO_ABS" ] || { log "ERROR: GRO not found: $GRO_ABS"; exit 1; }
    [ -f "$TRJ_ABS" ] || { log "ERROR: TRJ not found: $TRJ_ABS"; exit 1; }
    
    python3 "$PY_SCRIPTS/msd.py" \
        -s "$GRO_ABS" -f "$TRJ_ABS" \
        -o msd.xvg \
        --selection "${MSD_SELECTION:-name CA}" 2>&1 | tail -5
    
    if [ -f msd.xvg ]; then
        echo "  ✅ msd.xvg ($(wc -c < msd.xvg) bytes)"
    else
        echo "  ⚠️ MSD failed"
    fi
fi

# --- Residue Pair Distances ---
if [ "${SKIP_DIST:-0}" != "1" ]; then
    log "=== Distance: Residue pairs ==="
    
    if [ -n "$DIST_PAIRS" ]; then
        PAIRS=($DIST_PAIRS)
    else
        PAIRS=("160-206" "206-237" "160-237")
    fi
    
    python3 "$PY_SCRIPTS/distance.py" \
        -s "$GRO_ABS" -f "$TRJ_ABS" \
        -o distance \
        -p "${PAIRS[@]}" 2>&1 | grep -E '^\[DIST\]' | tail -10
    
    ls dist_*.xvg 2>/dev/null && echo "  ✅ distance files ready" || echo "  ⚠️ No distance files"
fi

# --- Chi Angles ---
if [ "${SKIP_CHI:-0}" != "1" ]; then
    log "=== Chi: Side-chain angles ==="
    
    RESIDS="${CHI_RESIDUES:-all}"
    python3 "$PY_SCRIPTS/chi.py" \
        -s "$GRO_ABS" -f "$TRJ_ABS" \
        -o chi \
        -r "$RESIDS" 2>&1 | grep -E 'chi1|chi2' | head -10
    
    ls chi_*.xvg 2>/dev/null && echo "  ✅ chi files ready" || echo "  ⚠️ No chi files"
fi

# --- Summary ---
log "=== Analysis complete ==="
echo "Output: $OUTPUT/"
ls -la *.xvg 2>/dev/null | awk '{print "  " $5 " " $NF}'

cat > ANALYSIS_REPORT.md << EOF
# Extended Analysis Report

## Diffusion (MSD)
- File: \`msd.xvg\`
- Note: Requires ≥ 10 ns trajectory for reliable D

## Residue Distances
- Files: \`dist_*.xvg\`
- Pairs: ${PAIRS[*]:-catalytic triad}

## Chi Angles
- Files: \`chi_chi1.xvg\`, \`chi_chi2.xvg\`
- Residues: ${CHI_RESIDUES:-all}

---
Generated: $(date)
EOF

log "✅ Extended analysis done"
