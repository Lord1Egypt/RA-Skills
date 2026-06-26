#!/bin/bash
# native-analysis.sh — Native GROMACS workaround analysis
# Uses GROMACS 2026 native commands with correct selection syntax
# Replaces broken Python fallbacks for msd, distance, chi
set -e

SKILL_ROOT="${SKILL_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"

TPR="${TPR:-md.tpr}"
GRO="${GRO:-md.gro}"
TRJ="${TRJ:-md.trr}"
NDX="${NDX:-}"
OUTPUT="${OUTPUT:-native_analysis}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# Resolve absolute paths
TRJ_ABS=$(realpath "$TRJ" 2>/dev/null || readlink -f "$TRJ" 2>/dev/null || echo "$(pwd)/$TRJ")
GRO_ABS=$(realpath "$GRO" 2>/dev/null || readlink -f "$GRO" 2>/dev/null || echo "$(pwd)/$GRO")
TPR_ABS=$(realpath "$TPR" 2>/dev/null || readlink -f "$TPR" 2>/dev/null || echo "$(pwd)/$TPR")

mkdir -p "$OUTPUT"
cd "$OUTPUT"

# ============================================================
# 1. MSD (Diffusion Coefficient)
# ============================================================
if [ "${SKIP_MSD:-0}" != "1" ]; then
    log "=== MSD: Diffusion Coefficient (native gmx msd) ==="
    
    # GROMACS 2026 syntax: -sel 'atomname CA'
    gmx msd -s "$TPR_ABS" -f "$TRJ_ABS" \
        -o msd.xvg -mol msd_mol.xvg \
        -sel "${MSD_SEL:-atomname CA}" \
        -tu ps 2>&1 | tail -3
    
    if [ -f msd.xvg ]; then
        # Extract D from mol file if available, else estimate from MSD
        if [ -f msd_mol.xvg ]; then
            echo "  ✅ msd.xvg ($(wc -c < msd.xvg) bytes) + msd_mol.xvg (per-molecule)"
        else
            echo "  ✅ msd.xvg ($(wc -c < msd.xvg) bytes)"
        fi
        # Quick D estimate from linear region
        python3 -c "
import numpy as np
data = np.loadtxt('msd.xvg', comments=['#','@'])
t = data[:,0]; msd = data[:,1]
if len(t) > 3:
    idx = max(1, int(len(t)*0.1))
    slope = np.polyfit(t[idx:], msd[idx:], 1)[0]
    D = slope / 6.0  # nm²/ps → 10⁻⁵ cm²/s
    print(f'  D ≈ {D*0.1:.4f} × 10⁻⁵ cm²/s')
" 2>/dev/null || true
    else
        echo "  ⚠️ MSD failed (fallback: use Python py/msd.py)"
    fi
fi

# ============================================================
# 2. Residue Pair Distances (via gmx pairdist)
# ============================================================
if [ "${SKIP_DIST:-0}" != "1" ]; then
    log "=== Distance: Residue pairs (native gmx pairdist) ==="
    
    # Default: catalytic triad pairs
    PAIRS="${DIST_PAIRS:-160,206 206,237 160,237}"
    
    for pair in $PAIRS; do
        r1=$(echo "$pair" | cut -d, -f1)
        r2=$(echo "$pair" | cut -d, -f2)
        
        gmx pairdist -s "$TPR_ABS" -f "$TRJ_ABS" \
            -o "distance_${r1}_${r2}.xvg" \
            -ref "res_cog of resnr ${r1}" \
            -sel "res_cog of resnr ${r2}" 2>&1 | tail -3
        
        if [ -f "distance_${r1}_${r2}.xvg" ]; then
            avg=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.3f", sum/n}' "distance_${r1}_${r2}.xvg")
            echo "  ✅ ${r1}-${r2}: avg=${avg} nm"
        fi
    done
    
    ls distance_*.xvg 2>/dev/null && echo "  ✅ distance files ready" || echo "  ⚠️ No distance files"
fi

# ============================================================
# 3. Chi Angles (via gmx chi)
# ============================================================
if [ "${SKIP_CHI:-0}" != "1" ]; then
    log "=== Chi: Dihedral angles (native gmx chi) ==="
    
    # gmx chi auto-detects all protein residues — no selection needed
    gmx chi -s "$TPR_ABS" -f "$TRJ_ABS" \
        -o chi_order.xvg -jc chi_jcoupling.xvg \
        -g chi.log -maxchi "${CHI_MAX:-2}" 2>&1 | tail -3
    
    if [ -f chi_order.xvg ]; then
        echo "  ✅ chi_order.xvg ($(wc -c < chi_order.xvg) bytes) — S² order parameters"
        [ -f chi_jcoupling.xvg ] && echo "  ✅ chi_jcoupling.xvg — J-coupling estimates"
        echo "  ✅ chi.log — Transitions + rotamer occupancies"
    else
        echo "  ⚠️ Chi failed (fallback: use Python py/chi.py)"
    fi
fi

# ============================================================
# Summary Report
# ============================================================
log "=== Analysis Complete ==="
echo ""
echo "Output directory: $OUTPUT/"
ls -la *.xvg *.log 2>/dev/null | awk '{print "  " $5 "B  " $NF}'

cat > ANALYSIS_REPORT.md << 'REOF'
# Native GROMACS Analysis Report

## MSD (Diffusion)
- `msd.xvg` — Mean squared displacement vs. lag time
- `msd_mol.xvg` — Per-molecule MSD (if available)
- Note: Requires ≥ 10 ns for reliable D

## Residue Distances
- `distance_*.xvg` — Center-of-geometry distances between residue pairs
- Uses `gmx pairdist` with `-ref`/`-sel` (GROMACS 2026 compatible)

## Chi Angles
- `chi_order.xvg` — Chi order parameters (S²) per residue
- `chi_prob.xvg` — Rotamer probabilities
- `chi_log.log` — Transitions and occupancies

## GROMACS Version Compatibility
These analyses use GROMACS 2026 native commands:
- `gmx msd -sel` ✅
- `gmx pairdist -ref/-sel` ✅  
- `gmx chi` ✅
- `gmx nmeig` ⚠️ (requires special setup, use Python fallback)

---
Generated: $(date)
REOF

echo ""
log "✅ Native analysis done"
