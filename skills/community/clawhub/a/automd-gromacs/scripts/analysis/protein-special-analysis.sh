#!/bin/bash
# protein-special-analysis - Advanced protein-focused analysis toolkit
# Covers DSSP, Ramachandran/chi, helix geometry, salt bridges, helix bundles,
# key residue summarization, and Markdown report generation.

set -euo pipefail

INPUT_TPR="${INPUT_TPR:-}"
INPUT_TRJ="${INPUT_TRJ:-}"
INPUT_NDX="${INPUT_NDX:-}"
OUTPUT_DIR="${OUTPUT_DIR:-protein-special-analysis}"
ANALYSIS_TYPE="${ANALYSIS_TYPE:-dssp,dihedral,helix,saltbridge,bundle,keyres,report}"
PROTEIN_GROUP="${PROTEIN_GROUP:-Protein}"
BACKBONE_GROUP="${BACKBONE_GROUP:-Backbone}"
CALPHA_GROUP="${CALPHA_GROUP:-C-alpha}"
HELIX_GROUP="${HELIX_GROUP:-Protein}"
HELIX_RESIDUES="${HELIX_RESIDUES:-}"
BUNDLE_GROUP="${BUNDLE_GROUP:-Protein}"
BUNDLE_NHELICES="${BUNDLE_NHELICES:-4}"
SALTBR_CUTOFF="${SALTBR_CUTOFF:-0.40}"
SALTBR_GROUP1="${SALTBR_GROUP1:-Protein}"
SALTBR_GROUP2="${SALTBR_GROUP2:-Protein}"
BEGIN_TIME="${BEGIN_TIME:-}"
END_TIME="${END_TIME:-}"
SKIP_FRAMES="${SKIP_FRAMES:-1}"
FORCE_REPORT="${FORCE_REPORT:-false}"

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
    [[ -f "$1" ]] || error "文件不存在: $1"
}

have_cmd() {
    command -v "$1" >/dev/null 2>&1
}

need_dssp() {
    have_cmd dssp || have_cmd mkdssp
}

time_opts() {
    local opts=""
    [[ -n "$BEGIN_TIME" ]] && opts="$opts -b $BEGIN_TIME"
    [[ -n "$END_TIME" ]] && opts="$opts -e $END_TIME"
    [[ "$SKIP_FRAMES" != "1" ]] && opts="$opts -dt $SKIP_FRAMES"
    echo "$opts"
}

run_cmd() {
    local logfile="$1"
    shift
    "$@" >"$logfile" 2>&1 || return 1
}

extract_xy_stats() {
    local file="$1"
    [[ -f "$file" ]] || return 0
    awk 'BEGIN{n=0; min=""; max=""}
         !/^[@#]/ && NF>=2 {
             v=$2; sum+=v; n++;
             if(min=="" || v<min) min=v;
             if(max=="" || v>max) max=v;
         }
         END {
             if(n>0) printf "avg=%.4f min=%.4f max=%.4f n=%d\n", sum/n, min, max, n;
         }' "$file"
}

extract_top_residues() {
    local file="$1"
    local limit="${2:-8}"
    [[ -f "$file" ]] || return 0
    awk '!/^[@#]/ && NF>=2 {printf "%s %.6f\n", $1, $2}' "$file" | sort -k2,2nr | head -n "$limit"
}

write_note() {
    local file="$1"
    shift
    printf '%s\n' "$@" > "$file"
}

show_help() {
    cat <<'EOF'
protein-special-analysis - Advanced protein-focused GROMACS analysis

USAGE:
  protein-special-analysis -s md.tpr -f md.xtc [OPTIONS]

ANALYSIS TYPES:
  dssp        - Secondary structure evolution via DSSP
  dihedral    - Enhanced Ramachandran / chi analysis
  helix       - Helix geometry/orientation/wheel analysis
  saltbridge  - Salt bridge analysis
  bundle      - Multi-helix bundle / axial tilt analysis
  keyres      - Key residue summary from structural change signals
  report      - Markdown report generation

OPTIONS:
  -s FILE             Structure/TPR file (required)
  -f FILE             Trajectory file (required)
  -n FILE             Index file (optional)
  -o DIR              Output directory (default: protein-special-analysis)
  --type LIST         Comma-separated analysis types
  --protein-group G   Protein group (default: Protein)
  --backbone-group G  Backbone group (default: Backbone)
  --calpha-group G    C-alpha group (default: C-alpha)
  --helix-group G     Group for helix analysis (default: Protein)
  --helix-residues R  Residue range label for helix subsets (e.g. 10-35,50-72)
  --bundle-group G    Group for bundle analysis (default: Protein)
  --bundle-nhelices N Number of helices in bundle (default: 4)
  --salt-cutoff D     Salt bridge cutoff in nm (default: 0.40)
  --salt-group1 G     First group for salt bridge analysis
  --salt-group2 G     Second group for salt bridge analysis
  -b TIME             Begin time in ps
  -e TIME             End time in ps
  --skip N            Analyze every Nth ps/frame stride hint (default: 1)
  --force-report      Generate report even if some analyses fail
  -h, --help          Show help

EXAMPLES:
  protein-special-analysis -s md.tpr -f md.xtc
  protein-special-analysis -s md.tpr -f md.xtc --type dssp,dihedral,report
  protein-special-analysis -s md.tpr -f md.xtc --helix-residues 10-35,43-68 --bundle-nhelices 2
  protein-special-analysis -s md.tpr -f md.xtc --salt-group1 Protein --salt-group2 Protein

WORKFLOW POSITIONING:
  - Use after basic `analysis.sh` when you need protein-specific interpretation.
  - Complements `advanced-analysis.sh`: that script focuses on PCA/cluster/contact/FEL,
    while this script focuses on secondary structure, helix physics, salt bridges,
    bundle organization, and residue-level mechanistic summaries.
EOF
}

validate_inputs() {
    [[ -n "$INPUT_TPR" ]] || error "缺少 -s <tpr_file>"
    [[ -n "$INPUT_TRJ" ]] || error "缺少 -f <trajectory_file>"
    check_file "$INPUT_TPR"
    check_file "$INPUT_TRJ"
    [[ -n "$INPUT_NDX" ]] && check_file "$INPUT_NDX"
    have_cmd gmx || error "gmx 未安装或不在 PATH 中"

    if awk "BEGIN{exit !($SALTBR_CUTOFF < 0.25)}"; then
        warn "盐桥 cutoff 过小，自动调整到 0.35 nm"
        SALTBR_CUTOFF="0.35"
    fi
    if awk "BEGIN{exit !($SALTBR_CUTOFF > 0.60)}"; then
        warn "盐桥 cutoff 过大，自动调整到 0.45 nm"
        SALTBR_CUTOFF="0.45"
    fi
}

run_dssp_analysis() {
    local outdir="$OUTPUT_DIR/dssp"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== DSSP 二级结构时间演化 ==="

    if ! need_dssp; then
        write_note "$outdir/STATUS.txt" "SKIPPED: DSSP/mkdssp not found" "Fix: sudo apt-get install dssp"
        warn "DSSP 未安装，跳过二级结构分析"
        return 0
    fi

    local opts
    opts="$(time_opts)"
    if echo "$PROTEIN_GROUP" | gmx do_dssp -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -o "$outdir/dssp.xpm" -sc "$outdir/dssp_summary.xvg" $opts >"$outdir/do_dssp.log" 2>&1; then
        awk 'BEGIN{helix=0; sheet=0; coil=0; n=0}
             !/^[@#]/ && NF>=5 {helix+=$2+$3+$4; sheet+=$5+$6; coil+=$7+$8+$9; n++}
             END {
                 if(n>0) {
                     printf "helix_avg=%.2f\n", helix/n;
                     printf "sheet_avg=%.2f\n", sheet/n;
                     printf "coil_avg=%.2f\n", coil/n;
                 }
             }' "$outdir/dssp_summary.xvg" > "$outdir/dssp_metrics.txt" || true
        cat > "$outdir/INTERPRETATION.txt" <<'EOF'
Interpretation hints:
- Helix fraction stable: folded helical core preserved.
- Sheet fraction stable: beta-core remains intact.
- Coil increase: possible local unfolding or hinge activation.
- Sudden helix/sheet loss with RMSD jump: check transition window and key residues.
EOF
    else
        write_note "$outdir/STATUS.txt" "FAILED: gmx do_dssp failed" "Check log: do_dssp.log"
        warn "DSSP 分析失败，详见 $outdir/do_dssp.log"
    fi
}

run_dihedral_analysis() {
    local outdir="$OUTPUT_DIR/dihedral"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== Ramachandran / chi 增强分析 ==="
    local opts
    opts="$(time_opts)"

    if echo "$BACKBONE_GROUP" | gmx rama -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -o "$outdir/ramachandran.xvg" -xpm "$outdir/ramachandran.xpm" $opts >"$outdir/rama.log" 2>&1; then
        awk '!/^[@#]/ && NF>=2 {
                 phi=$1; psi=$2; n++;
                 if(phi>=-160 && phi<=-30 && psi>=-90 && psi<=45) alpha++;
                 else if(((phi>=-180 && phi<=-45) && ((psi>=90 && psi<=180) || (psi>=-180 && psi<=-120)))) beta++;
                 else out++;
             }
             END {
                 if(n>0) {
                     printf "frames=%d\nalpha_like=%.2f\nbeta_like=%.2f\noutlier=%.2f\n", n, 100*alpha/n, 100*beta/n, 100*out/n;
                 }
             }' "$outdir/ramachandran.xvg" > "$outdir/rama_stats.txt" || true
    else
        write_note "$outdir/rama_status.txt" "FAILED: gmx rama failed" "Likely non-protein or missing backbone atoms"
        warn "Ramachandran 分析失败"
    fi

    if echo "$PROTEIN_GROUP" | gmx chi -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -o "$outdir/chi_angles.xvg" -all "$outdir/chi_all.xvg" -p "$outdir/chi_hist.xvg" -ss "$outdir/chi_order.xvg" $opts >"$outdir/chi.log" 2>&1; then
        extract_xy_stats "$outdir/chi_order.xvg" > "$outdir/chi_stats.txt" || true
    else
        write_note "$outdir/chi_status.txt" "FAILED: gmx chi failed" "Gly/Ala-rich systems may have limited chi information"
        warn "Chi 角分析失败或信息有限"
    fi

    cat > "$outdir/INTERPRETATION.txt" <<'EOF'
Interpretation hints:
- Ramachandran outlier > 5-10%: inspect whether outliers localize to loops or active-site turns.
- Persistent outliers inside long helices/sheets often indicate strain, poor sampling, or functionally relevant distortion.
- High chi-order usually means side chains are locked; low order suggests rotameric switching or pocket breathing.
EOF
}

run_helix_analysis() {
    local outdir="$OUTPUT_DIR/helix"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== 螺旋参数 / helixorient / wheel ==="
    local opts
    opts="$(time_opts)"

    if echo "$HELIX_GROUP" | gmx helix -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -to "$outdir/helix_order.xvg" -tz "$outdir/helix_twist.xvg" -or "$outdir/helix_radius.xvg" $opts >"$outdir/helix.log" 2>&1; then
        extract_xy_stats "$outdir/helix_order.xvg" > "$outdir/helix_order_stats.txt" || true
        extract_xy_stats "$outdir/helix_twist.xvg" > "$outdir/helix_twist_stats.txt" || true
    else
        write_note "$outdir/helix_status.txt" "FAILED: gmx helix failed" "Check helix group or residue range"
        warn "Helix 参数分析失败"
    fi

    if echo "$HELIX_GROUP" | gmx helixorient -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -oaxis "$outdir/helix_axis.xvg" -oc "$outdir/helix_center.xvg" -or "$outdir/helix_tilt.xvg" $opts >"$outdir/helixorient.log" 2>&1; then
        extract_xy_stats "$outdir/helix_tilt.xvg" > "$outdir/helix_tilt_stats.txt" || true
    else
        write_note "$outdir/helixorient_status.txt" "FAILED: gmx helixorient failed" "Often caused by non-helical selections or broken continuity"
        warn "Helixorient 分析失败"
    fi

    if [[ -n "$HELIX_RESIDUES" ]]; then
        if echo "$HELIX_GROUP" | gmx wheel -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
            -o "$outdir/helix_wheel.xvg" $opts >"$outdir/wheel.log" 2>&1; then
            write_note "$outdir/wheel_status.txt" "Wheel generated for residues: $HELIX_RESIDUES"
        else
            write_note "$outdir/wheel_status.txt" "FAILED: gmx wheel failed" "Wheel output depends on clean helix residue selection"
            warn "Helix wheel 生成失败"
        fi
    else
        write_note "$outdir/wheel_status.txt" "SKIPPED: add --helix-residues for wheel-focused interpretation"
    fi

    cat > "$outdir/INTERPRETATION.txt" <<'EOF'
Interpretation hints:
- Helix order drop + tilt increase often marks hinge opening or partial unwinding.
- Twist fluctuations are normal at helix ends; persistent large shifts in the middle usually deserve inspection.
- Wheel patterns help identify amphipathic helices; segregated hydrophobic/polar faces support membrane or interface function.
EOF
}

run_saltbridge_analysis() {
    local outdir="$OUTPUT_DIR/saltbridge"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== 盐桥分析 ==="
    local opts
    opts="$(time_opts)"

    if echo "$SALTBR_GROUP1 $SALTBR_GROUP2" | gmx saltbr -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -t "$SALTBR_CUTOFF" -num "$outdir/saltbridge_count.xvg" -dist "$outdir/saltbridge_dist.xvg" $opts >"$outdir/saltbr.log" 2>&1; then
        extract_xy_stats "$outdir/saltbridge_count.xvg" > "$outdir/saltbridge_stats.txt" || true
        extract_xy_stats "$outdir/saltbridge_dist.xvg" > "$outdir/saltbridge_dist_stats.txt" || true
    else
        write_note "$outdir/STATUS.txt" "FAILED: gmx saltbr failed" "Check charged residues and group selections"
        warn "盐桥分析失败"
    fi

    cat > "$outdir/INTERPRETATION.txt" <<EOF
Interpretation hints:
- Distance < ${SALTBR_CUTOFF} nm sustained over time suggests stable electrostatic locking.
- Bridge count drops before secondary-structure loss can indicate early destabilization.
- New long-lived salt bridges may reflect adaptive rearrangement or state switching.
EOF
}

run_bundle_analysis() {
    local outdir="$OUTPUT_DIR/bundle"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== 多螺旋束 / 轴向倾斜分析 ==="
    local opts
    opts="$(time_opts)"

    if echo "$BUNDLE_GROUP" | gmx bundle -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -na "$BUNDLE_NHELICES" -o "$outdir/bundle_tilt.xvg" -od "$outdir/bundle_dist.xvg" -oz "$outdir/bundle_z.xvg" $opts >"$outdir/bundle.log" 2>&1; then
        extract_xy_stats "$outdir/bundle_tilt.xvg" > "$outdir/bundle_tilt_stats.txt" || true
        extract_xy_stats "$outdir/bundle_dist.xvg" > "$outdir/bundle_dist_stats.txt" || true
    else
        write_note "$outdir/STATUS.txt" "FAILED: gmx bundle failed" "Bundle analysis requires well-defined helices and ordering"
        warn "Bundle 分析失败"
    fi

    cat > "$outdir/INTERPRETATION.txt" <<'EOF'
Interpretation hints:
- Small, stable inter-helix distances imply a tight bundle core.
- Increased axial tilt or bundle spread suggests gating, breathing, or membrane adaptation.
- If only one helix moves while others stay stable, inspect that helix's salt bridges and chi transitions.
EOF
}

run_keyres_analysis() {
    local outdir="$OUTPUT_DIR/keyres"
    local ndx_opts=()
    [[ -n "$INPUT_NDX" ]] && ndx_opts=(-n "$INPUT_NDX")
    mkdir -p "$outdir"
    log "=== 构象变化关键残基总结 ==="
    local opts
    opts="$(time_opts)"

    if echo "$CALPHA_GROUP" | gmx rmsf -s "$INPUT_TPR" -f "$INPUT_TRJ" "${ndx_opts[@]}" \
        -o "$outdir/rmsf_residue.xvg" -res $opts >"$outdir/rmsf.log" 2>&1; then
        extract_xy_stats "$outdir/rmsf_residue.xvg" > "$outdir/rmsf_stats.txt" || true
        extract_top_residues "$outdir/rmsf_residue.xvg" 12 > "$outdir/top_rmsf_residues.txt" || true
    else
        write_note "$outdir/rmsf_status.txt" "FAILED: gmx rmsf failed" "Check selection group"
    fi

    if [[ -f "$OUTPUT_DIR/dihedral/chi_order.xvg" ]]; then
        cp "$OUTPUT_DIR/dihedral/chi_order.xvg" "$outdir/chi_order_reused.xvg"
    fi
    if [[ -f "$OUTPUT_DIR/dssp/dssp_summary.xvg" ]]; then
        cp "$OUTPUT_DIR/dssp/dssp_summary.xvg" "$outdir/dssp_summary_reused.xvg"
    fi

    {
        echo "# Key residue summary"
        echo
        if [[ -f "$outdir/top_rmsf_residues.txt" ]]; then
            echo "## Highest-RMSF residues"
            awk '{printf "- Residue %s: RMSF %.3f nm\n", $1, $2}' "$outdir/top_rmsf_residues.txt"
            echo
        fi

        echo "## Mechanistic rules"
        echo "- High RMSF + local DSSP loss: likely hinge or unfolding hotspot."
        echo "- High RMSF + persistent helix retained: mobile but structured regulatory element."
        echo "- New salt bridge + lower local RMSF: stabilizing lock may form during transition."
        echo "- Chi disorder increase near pocket/interface: side-chain gating or packing rearrangement."
        echo

        echo "## Suggested inspection priority"
        if [[ -f "$outdir/top_rmsf_residues.txt" ]]; then
            awk 'NR<=5 {printf "%d. Residue %s because RMSF is high (%.3f nm).\n", NR, $1, $2}' "$outdir/top_rmsf_residues.txt"
        else
            echo "1. Inspect regions with secondary-structure conversion or helix tilt change."
        fi
    } > "$outdir/KEY_RESIDUES.md"
}

generate_report() {
    local report="$OUTPUT_DIR/PROTEIN_SPECIAL_REPORT.md"
    mkdir -p "$OUTPUT_DIR"
    log "=== 生成蛋白分析 Markdown 报告 ==="

    {
        echo "# Protein Special Analysis Report"
        echo
        echo "- Generated: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "- Structure: $INPUT_TPR"
        echo "- Trajectory: $INPUT_TRJ"
        echo "- Analysis types: $ANALYSIS_TYPE"
        echo "- Time range: ${BEGIN_TIME:-0} - ${END_TIME:-end} ps"
        echo
        echo "## Positioning"
        echo "- Use with basic \\`analysis.sh\\` for RMSD/RMSF/Rg baseline."
        echo "- Use with \\`advanced-analysis.sh\\` when PCA/FEL/cluster insight is also needed."
        echo

        echo "## Executive Summary"
        if [[ -f "$OUTPUT_DIR/dssp/dssp_metrics.txt" ]]; then
            echo "- Secondary structure metrics:"; sed 's/^/  - /' "$OUTPUT_DIR/dssp/dssp_metrics.txt"
        else
            echo "- Secondary structure: unavailable or skipped."
        fi
        if [[ -f "$OUTPUT_DIR/dihedral/rama_stats.txt" ]]; then
            echo "- Ramachandran summary:"; sed 's/^/  - /' "$OUTPUT_DIR/dihedral/rama_stats.txt"
        else
            echo "- Ramachandran summary: unavailable."
        fi
        if [[ -f "$OUTPUT_DIR/helix/helix_tilt_stats.txt" ]]; then
            echo "- Helix tilt summary:"; sed 's/^/  - /' "$OUTPUT_DIR/helix/helix_tilt_stats.txt"
        fi
        if [[ -f "$OUTPUT_DIR/saltbridge/saltbridge_stats.txt" ]]; then
            echo "- Salt bridge summary:"; sed 's/^/  - /' "$OUTPUT_DIR/saltbridge/saltbridge_stats.txt"
        fi
        if [[ -f "$OUTPUT_DIR/bundle/bundle_tilt_stats.txt" ]]; then
            echo "- Bundle tilt summary:"; sed 's/^/  - /' "$OUTPUT_DIR/bundle/bundle_tilt_stats.txt"
        fi
        echo

        echo "## Detailed Findings"
        for section in dssp dihedral helix saltbridge bundle; do
            if [[ -d "$OUTPUT_DIR/$section" ]]; then
                echo "### $section"
                if [[ -f "$OUTPUT_DIR/$section/INTERPRETATION.txt" ]]; then
                    sed 's/^/- /' "$OUTPUT_DIR/$section/INTERPRETATION.txt"
                else
                    echo "- No interpretation available."
                fi
                echo
            fi
        done

        echo "## Key Residues"
        if [[ -f "$OUTPUT_DIR/keyres/KEY_RESIDUES.md" ]]; then
            cat "$OUTPUT_DIR/keyres/KEY_RESIDUES.md"
        else
            echo "- No residue summary generated."
        fi
        echo

        echo "## Typical Interpretation Guide"
        echo "- Stable helix/sheet fractions + low tilt drift: folded state preserved."
        echo "- DSSP transition + Ramachandran outlier rise + salt bridge loss: strong evidence for local conformational switching."
        echo "- Bundle opening without widespread DSSP loss: functional breathing is more likely than unfolding."
        echo "- Side-chain disorder near catalytic/interface residues often points to gating rather than backbone collapse."
        echo

        echo "## Output Files"
        find "$OUTPUT_DIR" -maxdepth 2 -type f | sort | sed "s#^$OUTPUT_DIR/#- #"
        echo
        echo "*Generated by AutoMD-GROMACS protein-special-analysis*"
    } > "$report"
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s) INPUT_TPR="$2"; shift 2 ;;
            -f) INPUT_TRJ="$2"; shift 2 ;;
            -n) INPUT_NDX="$2"; shift 2 ;;
            -o) OUTPUT_DIR="$2"; shift 2 ;;
            --type) ANALYSIS_TYPE="$2"; shift 2 ;;
            --protein-group) PROTEIN_GROUP="$2"; shift 2 ;;
            --backbone-group) BACKBONE_GROUP="$2"; shift 2 ;;
            --calpha-group) CALPHA_GROUP="$2"; shift 2 ;;
            --helix-group) HELIX_GROUP="$2"; shift 2 ;;
            --helix-residues) HELIX_RESIDUES="$2"; shift 2 ;;
            --bundle-group) BUNDLE_GROUP="$2"; shift 2 ;;
            --bundle-nhelices) BUNDLE_NHELICES="$2"; shift 2 ;;
            --salt-cutoff) SALTBR_CUTOFF="$2"; shift 2 ;;
            --salt-group1) SALTBR_GROUP1="$2"; shift 2 ;;
            --salt-group2) SALTBR_GROUP2="$2"; shift 2 ;;
            -b) BEGIN_TIME="$2"; shift 2 ;;
            -e) END_TIME="$2"; shift 2 ;;
            --skip) SKIP_FRAMES="$2"; shift 2 ;;
            --force-report) FORCE_REPORT="true"; shift ;;
            -h|--help) show_help; exit 0 ;;
            *) error "未知参数: $1" ;;
        esac
    done
}

main() {
    parse_args "$@"
    validate_inputs
    mkdir -p "$OUTPUT_DIR"

    IFS=',' read -r -a types <<< "$ANALYSIS_TYPE"
    for raw_type in "${types[@]}"; do
        type="$(echo "$raw_type" | awk '{gsub(/^ +| +$/, ""); print}')"
        case "$type" in
            dssp) run_dssp_analysis ;;
            dihedral) run_dihedral_analysis ;;
            helix) run_helix_analysis ;;
            saltbridge) run_saltbridge_analysis ;;
            bundle) run_bundle_analysis ;;
            keyres) run_keyres_analysis ;;
            report) : ;;
            "") : ;;
            *) warn "忽略未知分析类型: $type" ;;
        esac
    done

    if [[ "$ANALYSIS_TYPE" == *"report"* ]] || [[ "$FORCE_REPORT" == "true" ]]; then
        generate_report
    fi

    log "完成。建议联用: basic analysis + advanced-analysis + protein-special-analysis"
}

main "$@"
