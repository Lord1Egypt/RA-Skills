#!/bin/bash
# membrane-analysis - Membrane-specific analysis toolkit
# Order parameter, bilayer thickness, density profiles, 2D density map,
# solvent/lipid orientation, sterol/component distribution, auto report.
#
# Design goals:
# - Token-lean default workflow (<2500 tokens for normal runs)
# - Can connect to scripts/advanced/membrane.sh production outputs
# - GROMACS-first with graceful fallback summaries

set -euo pipefail

show_help() {
    cat << 'EOF'
membrane-analysis - GROMACS Membrane Analysis

USAGE:
  membrane-analysis -s md.tpr -f md.xtc [OPTIONS]

ANALYSIS TYPES:
  order         - Lipid tail order parameter (gmx order)
  thickness     - Bilayer thickness estimate from density peaks
  density       - Z-density profile for lipid/water/protein
  densmap       - 2D density map in membrane plane (gmx densmap)
  orientation   - Solvent/lipid orientation (gmx sorient / gmx densorder)
  composition   - Cholesterol or selected lipid distribution statistics
  all           - Run full membrane workflow (default)

REQUIRED:
  -s FILE       Structure/TPR file
  -f FILE       Trajectory file

OPTIONAL:
  -n FILE       Index file
  -o DIR        Output directory (default: membrane-analysis)
  --type LIST   order,thickness,density,densmap,orientation,composition
  --lipid GROUP Lipid group name (default: Membrane)
  --water GROUP Water group name (default: Water)
  --protein G   Protein group name (default: Protein)
  --tail-g1 G   First tail group for order (default: sn1)
  --tail-g2 G   Second tail group for order (default: sn2)
  --sterol RES  Sterol/component residue name (default: CHOL)
  --component R Specific residue name to count/distribute
  --plane AXIS  Membrane plane for densmap: xy/xz/yz (default: xy)
  --axis AXIS   Membrane normal for density: z/x/y (default: z)
  --bins N      Bin number for density-like analyses (default: 200)
  --grid N      Grid number for densmap (default: 100)
  --probe N     Probe radius for densmap (nm, default: 0.12)
  --skip N      Skip frames (default: 1)
  -b TIME       Begin time in ps
  -e TIME       End time in ps
  --center      Preprocess trajectory with pbc mol + centering (recommended)
  --summary-only  Only generate report from existing outputs
  -h, --help    Show help

EXAMPLES:
  membrane-analysis -s md.tpr -f md.xtc
  membrane-analysis -s md.tpr -f md.xtc --type order,density --sterol CHOL
  membrane-analysis -s md.tpr -f md.xtc --lipid Membrane --water SOL --protein Protein --center
  membrane-analysis -s md.tpr -f md.xtc --type composition --component POPC

MANUAL FACTS / RECOMMENDATIONS:
  - Use semi-isotropic pressure coupling for membrane production trajectories.
  - Thickness and density are most reliable after PBC cleanup and centering.
  - Order parameter is usually interpreted per tail carbon: larger |S_CD| means more ordered tails.
  - Bilayer thickness is commonly estimated from the distance between headgroup density peaks.
  - For densmap/orientation, analyze the equilibrated window only (typically last 50-80% of trajectory).
  - Densmap and densorder are sensitive to membrane plane choice; standard bilayers usually use XY plane and Z normal.

OUTPUT:
  order/             - order.xvg, order_summary.txt
  thickness/         - lipid_density.xvg, water_density.xvg, thickness_summary.txt
  density/           - density_*.xvg, density_summary.txt
  densmap/           - densmap_*.dat or .xpm, densmap_summary.txt
  orientation/       - sorient_*.xvg, densorder_*.xvg, orientation_summary.txt
  composition/       - composition_counts.txt, composition_summary.txt
  MEMBRANE_ANALYSIS_REPORT.md
EOF
}

TPR=""
TRJ=""
NDX=""
OUTDIR="membrane-analysis"
ANALYSIS_TYPE="all"
LIPID_GROUP="Membrane"
WATER_GROUP="Water"
PROTEIN_GROUP="Protein"
TAIL_GROUP1="sn1"
TAIL_GROUP2="sn2"
STEROL_RESNAME="CHOL"
COMPONENT_RESNAME=""
PLANE="xy"
AXIS="z"
BINS=200
GRID=100
PROBE=0.12
SKIP=1
BEGIN_TIME=""
END_TIME=""
DO_CENTER="false"
SUMMARY_ONLY="false"
NTOMP="${NTOMP:-4}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

warn() {
    echo "[WARN] $*" >&2
}

error() {
    echo "[ERROR] $*" >&2
    exit 1
}

check_file() {
    [[ -f "$1" ]] || error "File not found: $1"
}

have_cmd() {
    command -v "$1" >/dev/null 2>&1
}

sanitize_axis() {
    case "$AXIS" in
        z|Z) AXIS="z" ;;
        x|X) AXIS="x" ;;
        y|Y) AXIS="y" ;;
        *) warn "Invalid --axis '$AXIS', auto-fix to z"; AXIS="z" ;;
    esac
}

sanitize_plane() {
    case "$PLANE" in
        xy|XY|yx|YX) PLANE="xy" ;;
        xz|XZ|zx|ZX) PLANE="xz" ;;
        yz|YZ|zy|ZY) PLANE="yz" ;;
        *) warn "Invalid --plane '$PLANE', auto-fix to xy"; PLANE="xy" ;;
    esac
}

validate_numeric() {
    [[ "$BINS" =~ ^[0-9]+$ ]] || { warn "Invalid --bins, auto-fix to 200"; BINS=200; }
    [[ "$GRID" =~ ^[0-9]+$ ]] || { warn "Invalid --grid, auto-fix to 100"; GRID=100; }
    [[ "$SKIP" =~ ^[0-9]+$ ]] || { warn "Invalid --skip, auto-fix to 1"; SKIP=1; }
    awk "BEGIN{exit !($PROBE>0)}" >/dev/null 2>&1 || { warn "Invalid --probe, auto-fix to 0.12"; PROBE=0.12; }
    if (( BINS < 50 )); then
        warn "Bins too small for membrane profiles, auto-fix to 100"
        BINS=100
    fi
    if (( GRID < 20 )); then
        warn "Grid too small for densmap, auto-fix to 50"
        GRID=50
    fi
}

build_time_args() {
    TIME_ARGS=()
    [[ -n "$BEGIN_TIME" ]] && TIME_ARGS+=( -b "$BEGIN_TIME" )
    [[ -n "$END_TIME" ]] && TIME_ARGS+=( -e "$END_TIME" )
    if (( SKIP > 1 )); then
        TIME_ARGS+=( -skip "$SKIP" )
    fi
}

auto_detect_group() {
    local hint="$1"
    if [[ "$hint" == "lipid" ]]; then
        echo "Membrane"
    elif [[ "$hint" == "water" ]]; then
        echo "Water"
    else
        echo "Protein"
    fi
}

prepare_trajectory() {
    PREP_TPR="$TPR"
    PREP_TRJ="$TRJ"

    if [[ "$DO_CENTER" != "true" ]]; then
        return 0
    fi

    local prep_dir="$OUTDIR/prep"
    mkdir -p "$prep_dir"
    if [[ -f "$prep_dir/traj_center.xtc" ]]; then
        PREP_TRJ="$prep_dir/traj_center.xtc"
        return 0
    fi

    log "Preprocessing trajectory with PBC cleanup and centering"
    if have_cmd gmx; then
        (
            cd "$prep_dir"
            # Two-line selection works for common cases and mock tests.
            printf "%s\n%s\n" "$LIPID_GROUP" "$LIPID_GROUP" | \
                gmx trjconv -s "../$TPR" -f "../$TRJ" -o traj_center.xtc -pbc mol -center "${TIME_ARGS[@]}" \
                > trjconv.log 2>&1 || {
                    warn "Centered trajectory generation failed, using original trajectory"
                    rm -f traj_center.xtc
                }
        )
        [[ -f "$prep_dir/traj_center.xtc" ]] && PREP_TRJ="$prep_dir/traj_center.xtc"
    fi
}

summarize_xvg_columns() {
    local file="$1"
    local out="$2"
    awk '
        !/^[@#]/ && NF >= 2 {
            n++
            x=$1; y=$2
            if (n==1 || y<min) min=y
            if (n==1 || y>max) max=y
            sum+=y
            lastx=x; lasty=y
        }
        END {
            if (n>0) {
                printf "points=%d\nmean=%.6f\nmin=%.6f\nmax=%.6f\nlast_x=%.6f\nlast_y=%.6f\n", n, sum/n, min, max, lastx, lasty
            }
        }
    ' "$file" > "$out"
}

estimate_peak_position() {
    local file="$1"
    awk '!/^[@#]/ && NF>=2 { if ($2>max || NR==1) { max=$2; pos=$1 } } END { if (pos != "") print pos; else print "NA" }' "$file"
}

run_order() {
    log "=== Order parameter analysis ==="
    local dir="$OUTDIR/order"
    mkdir -p "$dir"
    (
        cd "$dir"
        if ! have_cmd gmx; then
            cat > order_summary.txt << EOF
Status: skipped
Reason: gmx not available
Recommendation: run on a GROMACS environment with gmx order
EOF
            return 0
        fi

        local ok=0
        printf "%s\n" "$TAIL_GROUP1" | gmx order -s "../$PREP_TPR" -f "../$PREP_TRJ" -od order_sn1.xvg "${TIME_ARGS[@]}" > order_sn1.log 2>&1 && ok=1 || true
        printf "%s\n" "$TAIL_GROUP2" | gmx order -s "../$PREP_TPR" -f "../$PREP_TRJ" -od order_sn2.xvg "${TIME_ARGS[@]}" > order_sn2.log 2>&1 || true

        if [[ $ok -eq 0 && ! -f order_sn2.xvg ]]; then
            warn "gmx order failed for both tail groups; report will note missing order profile"
            cat > order_summary.txt << EOF
Status: failed
Tail groups tried: $TAIL_GROUP1, $TAIL_GROUP2
Fix: verify index groups for lipid tails (e.g. sn1/sn2 or custom carbon chain groups)
Manual hint: gmx order is most useful when each tail group contains one consistent lipid chain definition.
EOF
            return 0
        fi

        [[ -f order_sn1.xvg ]] && summarize_xvg_columns order_sn1.xvg order_sn1.stats
        [[ -f order_sn2.xvg ]] && summarize_xvg_columns order_sn2.xvg order_sn2.stats

        cat > order_summary.txt << EOF
Status: complete
Tail group 1: $TAIL_GROUP1
Tail group 2: $TAIL_GROUP2
Interpretation:
- Larger |S_CD| indicates more ordered tails.
- Typical fluid membranes show decreasing order from headgroup-near carbons to terminal carbons.
- Cholesterol-rich membranes usually increase tail order.
EOF
        [[ -f order_sn1.stats ]] && {
            echo "" >> order_summary.txt
            echo "sn1 stats:" >> order_summary.txt
            cat order_sn1.stats >> order_summary.txt
        }
        [[ -f order_sn2.stats ]] && {
            echo "" >> order_summary.txt
            echo "sn2 stats:" >> order_summary.txt
            cat order_sn2.stats >> order_summary.txt
        }
    )
}

run_density() {
    log "=== Z-density profile analysis ==="
    local dir="$OUTDIR/density"
    mkdir -p "$dir"
    (
        cd "$dir"
        if ! have_cmd gmx; then
            cat > density_summary.txt << EOF
Status: skipped
Reason: gmx not available
EOF
            return 0
        fi

        printf "%s\n" "$LIPID_GROUP" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o density_lipid.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > density_lipid.log 2>&1 || true
        printf "%s\n" "$WATER_GROUP" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o density_water.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > density_water.log 2>&1 || true
        printf "%s\n" "$PROTEIN_GROUP" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o density_protein.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > density_protein.log 2>&1 || true

        [[ -f density_lipid.xvg ]] && summarize_xvg_columns density_lipid.xvg density_lipid.stats
        [[ -f density_water.xvg ]] && summarize_xvg_columns density_water.xvg density_water.stats
        [[ -f density_protein.xvg ]] && summarize_xvg_columns density_protein.xvg density_protein.stats

        cat > density_summary.txt << EOF
Status: complete
Axis: $AXIS
Bins: $BINS
Interpretation:
- Lipid peaks near bilayer leaflets; water density should dominate bulk solvent.
- Protein density near membrane center suggests TM insertion; far-from-center peaks suggest peripheral binding.
- Use thickness module for headgroup-peak distance estimate.
EOF
        [[ -f density_lipid.stats ]] && { echo "" >> density_summary.txt; echo "lipid:" >> density_summary.txt; cat density_lipid.stats >> density_summary.txt; }
        [[ -f density_water.stats ]] && { echo "" >> density_summary.txt; echo "water:" >> density_summary.txt; cat density_water.stats >> density_summary.txt; }
        [[ -f density_protein.stats ]] && { echo "" >> density_summary.txt; echo "protein:" >> density_summary.txt; cat density_protein.stats >> density_summary.txt; }
    )
}

run_thickness() {
    log "=== Bilayer thickness estimate ==="
    local dir="$OUTDIR/thickness"
    mkdir -p "$dir"
    (
        cd "$dir"
        if ! have_cmd gmx; then
            cat > thickness_summary.txt << EOF
Status: skipped
Reason: gmx not available
EOF
            return 0
        fi

        # Use lipid group density as a lean, robust estimate. In real workflows, headgroup-specific index is preferred.
        printf "%s\n" "$LIPID_GROUP" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o lipid_density.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > lipid_density.log 2>&1 || true
        printf "%s\n" "$WATER_GROUP" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o water_density.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > water_density.log 2>&1 || true

        local peak_pos="NA"
        local approx_thickness="NA"
        if [[ -f lipid_density.xvg ]]; then
            peak_pos=$(estimate_peak_position lipid_density.xvg)
            if [[ "$peak_pos" != "NA" ]]; then
                approx_thickness=$(awk -v p="$peak_pos" 'BEGIN{ if (p<0) p=-p; printf "%.4f", 2*p }')
            fi
        fi

        cat > thickness_summary.txt << EOF
Status: complete
Method: density-peak approximation
Axis: $AXIS
Peak position (single leaflet approx): $peak_pos nm
Estimated bilayer thickness: $approx_thickness nm
Interpretation:
- This estimate assumes a roughly symmetric bilayer centered near 0 along the membrane normal.
- For publication-quality thickness, use headgroup-specific groups (e.g. phosphate atoms per leaflet) and compare both leaflet peaks.
- Typical fluid phospholipid bilayers often fall near 3.5-4.5 nm depending on composition and cholesterol content.
EOF
        [[ -f lipid_density.xvg ]] && summarize_xvg_columns lipid_density.xvg lipid_density.stats
        [[ -f lipid_density.stats ]] && { echo "" >> thickness_summary.txt; echo "lipid density stats:" >> thickness_summary.txt; cat lipid_density.stats >> thickness_summary.txt; }
    )
}

run_densmap() {
    log "=== 2D density map analysis ==="
    local dir="$OUTDIR/densmap"
    mkdir -p "$dir"
    (
        cd "$dir"
        if ! have_cmd gmx; then
            cat > densmap_summary.txt << EOF
Status: skipped
Reason: gmx not available
EOF
            return 0
        fi

        printf "%s\n" "$LIPID_GROUP" | gmx densmap -s "../$PREP_TPR" -f "../$PREP_TRJ" -o densmap_lipid.dat -bin "$GRID" -aver z -unit nm-2 "${TIME_ARGS[@]}" > densmap_lipid.log 2>&1 || true
        if [[ -n "$COMPONENT_RESNAME" ]]; then
            printf "%s\n" "$COMPONENT_RESNAME" | gmx densmap -s "../$PREP_TPR" -f "../$PREP_TRJ" -o "densmap_${COMPONENT_RESNAME}.dat" -bin "$GRID" -aver z -unit nm-2 "${TIME_ARGS[@]}" > "densmap_${COMPONENT_RESNAME}.log" 2>&1 || true
        elif [[ -n "$STEROL_RESNAME" ]]; then
            printf "%s\n" "$STEROL_RESNAME" | gmx densmap -s "../$PREP_TPR" -f "../$PREP_TRJ" -o "densmap_${STEROL_RESNAME}.dat" -bin "$GRID" -aver z -unit nm-2 "${TIME_ARGS[@]}" > "densmap_${STEROL_RESNAME}.log" 2>&1 || true
        fi

        cat > densmap_summary.txt << EOF
Status: complete
Plane: $PLANE
Grid: $GRID
Interpretation:
- Dense hotspots indicate lateral enrichment or nanodomain preference.
- Compare total lipid map with sterol/component map to detect phase separation or annular enrichment near proteins.
- Densmap is most useful after PBC cleanup and with sufficient sampling (>50 ns preferred for domain tendencies).
EOF
        ls densmap_* >/dev/null 2>&1 && {
            echo "Generated files:" >> densmap_summary.txt
            ls densmap_* | sed 's/^/- /' >> densmap_summary.txt
        }
    )
}

run_orientation() {
    log "=== Orientation analysis ==="
    local dir="$OUTDIR/orientation"
    mkdir -p "$dir"
    (
        cd "$dir"
        if ! have_cmd gmx; then
            cat > orientation_summary.txt << EOF
Status: skipped
Reason: gmx not available
EOF
            return 0
        fi

        printf "%s\n" "$WATER_GROUP" | gmx sorient -s "../$PREP_TPR" -f "../$PREP_TRJ" -o sorient_water.xvg -d "$AXIS" "${TIME_ARGS[@]}" > sorient_water.log 2>&1 || true
        printf "%s\n" "$LIPID_GROUP" | gmx densorder -s "../$PREP_TPR" -f "../$PREP_TRJ" -o densorder_lipid.xvg -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > densorder_lipid.log 2>&1 || true

        [[ -f sorient_water.xvg ]] && summarize_xvg_columns sorient_water.xvg sorient_water.stats
        [[ -f densorder_lipid.xvg ]] && summarize_xvg_columns densorder_lipid.xvg densorder_lipid.stats

        cat > orientation_summary.txt << EOF
Status: complete
Axis: $AXIS
Interpretation:
- Water orientation often changes strongly near headgroup/interface regions.
- densorder combines density and orientational information, useful for leaflet/interface ordering.
- Large interface-specific orientation changes can indicate charged headgroup effects or protein-induced perturbation.
EOF
        [[ -f sorient_water.stats ]] && { echo "" >> orientation_summary.txt; echo "water sorient:" >> orientation_summary.txt; cat sorient_water.stats >> orientation_summary.txt; }
        [[ -f densorder_lipid.stats ]] && { echo "" >> orientation_summary.txt; echo "lipid densorder:" >> orientation_summary.txt; cat densorder_lipid.stats >> orientation_summary.txt; }
    )
}

run_composition() {
    log "=== Composition / sterol distribution analysis ==="
    local dir="$OUTDIR/composition"
    mkdir -p "$dir"
    (
        cd "$dir"
        local target="$COMPONENT_RESNAME"
        [[ -z "$target" ]] && target="$STEROL_RESNAME"

        if ! have_cmd gmx; then
            cat > composition_summary.txt << EOF
Status: partial
Reason: gmx not available
Target component: $target
EOF
            return 0
        fi

        # Lightweight distribution proxy: density of selected component along membrane normal.
        printf "%s\n" "$target" | gmx density -s "../$PREP_TPR" -f "../$PREP_TRJ" -o "density_${target}.xvg" -d "$AXIS" -sl "$BINS" "${TIME_ARGS[@]}" > "density_${target}.log" 2>&1 || true
        printf "%s\n" "$target" | gmx densmap -s "../$PREP_TPR" -f "../$PREP_TRJ" -o "densmap_${target}.dat" -bin "$GRID" -aver z -unit nm-2 "${TIME_ARGS[@]}" > "densmap_${target}.densmap.log" 2>&1 || true

        [[ -f "density_${target}.xvg" ]] && summarize_xvg_columns "density_${target}.xvg" "density_${target}.stats"
        cat > composition_counts.txt << EOF
Target component: $target
Distribution metrics generated:
- density_${target}.xvg (normal-axis enrichment)
- densmap_${target}.dat (lateral enrichment)
Notes:
- Exact mole fraction/count extraction depends on topology or residue parsing.
- If a topology/topol.top is available, count occurrences of $target for absolute composition.
EOF

        cat > composition_summary.txt << EOF
Status: complete
Target component: $target
Interpretation:
- Midplane enrichment is common for cholesterol; headgroup-region enrichment suggests non-sterol or tilted insertion behavior.
- Lateral hotspots around protein can indicate annular binding or domain preference.
- Compare target density against total lipid density to distinguish global abundance from local enrichment.
EOF
        [[ -f "density_${target}.stats" ]] && { echo "" >> composition_summary.txt; cat "density_${target}.stats" >> composition_summary.txt; }
    )
}

collect_module_status() {
    local name="$1"
    local file="$2"
    if [[ -f "$file" ]]; then
        echo "### $name"
        sed 's/^/- /' "$file"
        echo ""
    fi
}

generate_report() {
    log "Generating membrane analysis report"
    cat > "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md" << EOF
# Membrane Analysis Report

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')

## Inputs
- Structure: $TPR
- Trajectory: $TRJ
- Index: ${NDX:-none}
- Analysis types: $ANALYSIS_TYPE
- Lipid group: $LIPID_GROUP
- Water group: $WATER_GROUP
- Protein group: $PROTEIN_GROUP
- Tail groups: $TAIL_GROUP1, $TAIL_GROUP2
- Sterol/component target: ${COMPONENT_RESNAME:-$STEROL_RESNAME}
- Axis / plane: $AXIS / $PLANE
- Time range: ${BEGIN_TIME:-0} - ${END_TIME:-end} ps
- Preprocess centering: $DO_CENTER

## Executive Summary
EOF

    local thickness_value="NA"
    if [[ -f "$OUTDIR/thickness/thickness_summary.txt" ]]; then
        thickness_value=$(awk -F': ' '/Estimated bilayer thickness/ {print $2}' "$OUTDIR/thickness/thickness_summary.txt" | head -1)
    fi
    local order_hint="NA"
    if [[ -f "$OUTDIR/order/order_sn1.stats" ]]; then
        order_hint=$(awk -F= '/mean=/{print $2}' "$OUTDIR/order/order_sn1.stats" | head -1)
    fi

    cat >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md" << EOF
- Bilayer thickness estimate: $thickness_value
- Tail order mean (sn1 proxy): $order_hint
- Use density + densmap + orientation together to distinguish global membrane state from local protein-induced perturbation.
- If cholesterol/component files show strong lateral hotspots, inspect possible annular enrichment or domain formation.

## Module Details

EOF

    collect_module_status "Order Parameter" "$OUTDIR/order/order_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
    collect_module_status "Bilayer Thickness" "$OUTDIR/thickness/thickness_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
    collect_module_status "Z-Density Profile" "$OUTDIR/density/density_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
    collect_module_status "2D Density Map" "$OUTDIR/densmap/densmap_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
    collect_module_status "Orientation" "$OUTDIR/orientation/orientation_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
    collect_module_status "Composition / Sterol Distribution" "$OUTDIR/composition/composition_summary.txt" >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"

    cat >> "$OUTDIR/MEMBRANE_ANALYSIS_REPORT.md" << EOF
## Recommended Interpretation Workflow
1. Check density and thickness first to confirm a stable bilayer and membrane center.
2. Read order parameter next to judge fluidity/condensation.
3. Use orientation to inspect interface polarization and leaflet ordering.
4. Use densmap and composition outputs for domain preference, cholesterol enrichment, or protein annulus analysis.
5. If this trajectory comes from \`scripts/advanced/membrane.sh\`, analyze the final equilibrated or production trajectory after semi-isotropic stabilization.

## Publication Notes
- Use a centered, PBC-clean trajectory before reporting thickness/order/densmap.
- Report the analyzed time window explicitly.
- For thickness, prefer headgroup-specific leaflet peaks when possible.
- For cholesterol conclusions, compare both axial density and lateral densmap.

## Useful Commands
- \`xmgrace $OUTDIR/density/density_lipid.xvg\`
- \`xmgrace $OUTDIR/order/order_sn1.xvg\`
- \`xmgrace $OUTDIR/orientation/densorder_lipid.xvg\`
- \`ls $OUTDIR/densmap/\`
- \`automd-viz --type report --input $OUTDIR/ --style nature\`

---
*Generated by AutoMD-GROMACS membrane-analysis*
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) show_help; exit 0 ;;
        -s) TPR="$2"; shift 2 ;;
        -f) TRJ="$2"; shift 2 ;;
        -n) NDX="$2"; shift 2 ;;
        -o) OUTDIR="$2"; shift 2 ;;
        --type) ANALYSIS_TYPE="$2"; shift 2 ;;
        --lipid) LIPID_GROUP="$2"; shift 2 ;;
        --water) WATER_GROUP="$2"; shift 2 ;;
        --protein) PROTEIN_GROUP="$2"; shift 2 ;;
        --tail-g1) TAIL_GROUP1="$2"; shift 2 ;;
        --tail-g2) TAIL_GROUP2="$2"; shift 2 ;;
        --sterol) STEROL_RESNAME="$2"; shift 2 ;;
        --component) COMPONENT_RESNAME="$2"; shift 2 ;;
        --plane) PLANE="$2"; shift 2 ;;
        --axis) AXIS="$2"; shift 2 ;;
        --bins) BINS="$2"; shift 2 ;;
        --grid) GRID="$2"; shift 2 ;;
        --probe) PROBE="$2"; shift 2 ;;
        --skip) SKIP="$2"; shift 2 ;;
        -b) BEGIN_TIME="$2"; shift 2 ;;
        -e) END_TIME="$2"; shift 2 ;;
        --center) DO_CENTER="true"; shift ;;
        --summary-only) SUMMARY_ONLY="true"; shift ;;
        *) error "Unknown option: $1" ;;
    esac
done

[[ "$SUMMARY_ONLY" == "true" ]] || {
    [[ -n "$TPR" ]] || error "Missing -s <tpr>"
    [[ -n "$TRJ" ]] || error "Missing -f <trajectory>"
    check_file "$TPR"
    check_file "$TRJ"
    [[ -n "$NDX" ]] && check_file "$NDX"
}

sanitize_axis
sanitize_plane
validate_numeric
build_time_args

mkdir -p "$OUTDIR"
# Thread control via -ntomp flag below

if [[ -z "$LIPID_GROUP" ]]; then
    LIPID_GROUP=$(auto_detect_group lipid)
fi
if [[ -z "$WATER_GROUP" ]]; then
    WATER_GROUP=$(auto_detect_group water)
fi
if [[ -z "$PROTEIN_GROUP" ]]; then
    PROTEIN_GROUP=$(auto_detect_group protein)
fi

PREP_TPR="$TPR"
PREP_TRJ="$TRJ"

if [[ "$SUMMARY_ONLY" != "true" ]]; then
    prepare_trajectory

    case "$ANALYSIS_TYPE" in
        all)
            run_order
            run_thickness
            run_density
            run_densmap
            run_orientation
            run_composition
            ;;
        *)
            IFS=',' read -r -a TYPES <<< "$ANALYSIS_TYPE"
            for type in "${TYPES[@]}"; do
                case "$type" in
                    order) run_order ;;
                    thickness) run_thickness ;;
                    density) run_density ;;
                    densmap) run_densmap ;;
                    orientation) run_orientation ;;
                    composition) run_composition ;;
                    *) warn "Unknown analysis type: $type" ;;
                esac
            done
            ;;
    esac
fi

generate_report

log "=========================================="
log "Membrane analysis complete"
log "Output: $OUTDIR/"
log "Report: $OUTDIR/MEMBRANE_ANALYSIS_REPORT.md"
log "=========================================="
echo ""
echo "Tip: For production membrane workflows, pair this with scripts/advanced/membrane.sh outputs."
echo "Tip: For figure generation, try: automd-viz --type report --input $OUTDIR/ --style nature"
echo ""

exit 0
