#!/bin/bash
# GROMACS Extended Properties Analysis
# 蛋白高级性质: 偶极矩, 静电势, 自由体积, 水合层, 最小距离
# GROMACS 2026 compatible
set -e

TRJ="${TRJ:-md.trr}"
TPR="${TPR:-md.tpr}"
NDX="${NDX:-analysis.ndx}"
OUTPUT="${OUTPUT:-properties}"
ANALYSES="${ANALYSES:-dipoles,potential,freevolume,h2order,mindist}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
check_file() { [ -f "$1" ] || { echo "[ERROR] Missing: $1"; exit 1; }; }

# Check prerequisites
check_file "$TPR"
check_file "$TRJ"

# Create index if missing
if [ ! -f "$NDX" ]; then
    log "Creating index file..."
    echo "q" | gmx make_ndx -f "$TPR" -o "$NDX" 2>&1 | tail -1
fi

mkdir -p "$OUTPUT"
cd "$OUTPUT"

# Wrap GROMACS calls safely — no eval, pipe input explicitly
safe_run() {
    local input="$1"
    local cmd_desc="$2"
    local out="$3"
    shift 3
    log "Running: $cmd_desc"
    if printf '%s\n' "$input" | "$@" 2>&1 | tail -3; then
        log "  ✅ $out"
        return 0
    else
        log "  ⚠️ $out (non-fatal, continuing)"
        return 1
    fi
}

# Track which analyses actually produced output
DIPOLE_OK=0
POTENTIAL_OK=0
FREEVOL_OK=0
H2ORDER_OK=0
MINDIST_OK=0
SASA_OK=0

IFS=',' read -ra AN <<< "$ANALYSES"
for a in "${AN[@]}"; do
    case "$a" in
        dipoles)
            safe_run "Protein" "gmx dipoles ..." "dipoles.xvg" \
                gmx dipoles -s ../$TPR -f ../$TRJ -n ../$NDX -o dipoles.xvg -eps epsilon.xvg && DIPOLE_OK=1
            ;;
        potential)
            safe_run "Protein" "gmx potential ..." "potential.xvg" \
                gmx potential -s ../$TPR -f ../$TRJ -n ../$NDX -o potential.xvg && POTENTIAL_OK=1
            ;;
        freevolume)
            safe_run "Protein" "gmx freevolume ..." "freevolume.xvg" \
                gmx freevolume -s ../$TPR -f ../$TRJ -n ../$NDX -o freevolume.xvg && FREEVOL_OK=1
            ;;
        h2order)
            safe_run "Water_and_ions" "gmx h2order ..." "h2order.xvg" \
                gmx h2order -s ../$TPR -f ../$TRJ -n ../$NDX -o h2order.xvg && H2ORDER_OK=1
            ;;
        mindist)
            safe_run "Protein" "gmx mindist ..." "mindist.xvg" \
                gmx mindist -s ../$TPR -f ../$TRJ -n ../$NDX -od mindist.xvg && MINDIST_OK=1
            ;;
        sasa)
            safe_run "Protein" "gmx sasa ..." "sasa.xvg" \
                gmx sasa -s ../$TPR -f ../$TRJ -n ../$NDX -o sasa.xvg && SASA_OK=1
            ;;
    esac
done

# Generate report — only describe analyses that actually ran
log "Generating report..."

cat > PROPERTIES_REPORT.md << REOF
# Extended Protein Properties Report

Generated: $(date)

REOF

# Dipole Moment
if [[ $DIPOLE_OK -eq 1 ]]; then
cat >> PROPERTIES_REPORT.md << 'REOF'
## Dipole Moment
- File: `dipoles.xvg` — Total dipole moment (Debye) vs time
- File: `epsilon.xvg` — Dielectric constant estimate
- Interpretation: Large fluctuations indicate conformational changes

REOF
else
cat >> PROPERTIES_REPORT.md << 'REOF'
## Dipole Moment ⚠️
- Analysis was requested but did not complete successfully.
- Check logs for errors.

REOF
fi

# Electrostatic Potential
if [[ $POTENTIAL_OK -eq 1 ]]; then
cat >> PROPERTIES_REPORT.md << 'REOF'
## Electrostatic Potential
- File: `potential.xvg` — Potential along box Z-axis (mV)
- Use: Identify charged patches, membrane potential

REOF
else
cat >> PROPERTIES_REPORT.md << 'REOF'
## Electrostatic Potential ⚠️
- Analysis was requested but did not complete successfully.
- Check logs for errors.

REOF
fi

# Free Volume
if [[ $FREEVOL_OK -eq 1 ]]; then
cat >> PROPERTIES_REPORT.md << 'REOF'
## Free Volume
- File: `freevolume.xvg` — Molecular and van der Waals volumes
- Interpretation: >0.25 = flexible, <0.20 = rigid

REOF
else
cat >> PROPERTIES_REPORT.md << 'REOF'
## Free Volume ⚠️
- Analysis was requested but did not complete successfully.
- Check logs for errors.

REOF
fi

# Water Ordering
if [[ $H2ORDER_OK -eq 1 ]]; then
cat >> PROPERTIES_REPORT.md << 'REOF'
## Water Ordering (h2order)
- File: `h2order.xvg` — Water molecule orientation around protein
- Interpretation: High order near hydrophobic surfaces, low near charged

REOF
else
cat >> PROPERTIES_REPORT.md << 'REOF'
## Water Ordering ⚠️
- Analysis was requested but did not complete successfully.
- Check logs for errors.

REOF
fi

# Minimum Distance
if [[ $MINDIST_OK -eq 1 ]]; then
cat >> PROPERTIES_REPORT.md << 'REOF'
## Minimum Distance
- File: `mindist.xvg` — Closest contact distance between groups
- Use: Monitor binding/unbinding events, steric clashes

REOF
else
cat >> PROPERTIES_REPORT.md << 'REOF'
## Minimum Distance ⚠️
- Analysis was requested but did not complete successfully.
- Check logs for errors.

REOF
fi

log "✅ Properties analysis complete: $OUTPUT/"
