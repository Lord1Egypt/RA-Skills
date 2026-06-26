#!/bin/bash
# GROMACS free energy result analysis hub
# Supports BAR/FEP, WHAM/PMF, AWH, overlap/convergence/error estimation,
# and unified reporting across methods.

set -euo pipefail

MODE="${MODE:-all}"
INPUT_DIR="${INPUT_DIR:-.}"
OUTPUT_DIR="${OUTPUT_DIR:-free-energy-analysis}"
REPORT_NAME="${REPORT_NAME:-FREE_ENERGY_ANALYSIS_REPORT.md}"
BAR_INPUTS="${BAR_INPUTS:-}"
BAR_PATTERN="${BAR_PATTERN:-}"
WHAM_TPR_LIST="${WHAM_TPR_LIST:-}"
WHAM_PULLF_LIST="${WHAM_PULLF_LIST:-}"
PMF_FILE="${PMF_FILE:-}"
HIST_FILE="${HIST_FILE:-}"
AWH_EDR="${AWH_EDR:-}"
AWH_LOG="${AWH_LOG:-}"
AWH_PMF="${AWH_PMF:-}"
SERIES_FILE="${SERIES_FILE:-}"
TEMPERATURE="${TEMPERATURE:-300}"
BOOTSTRAP_SAMPLES="${BOOTSTRAP_SAMPLES:-200}"
BLOCK_COUNT="${BLOCK_COUNT:-5}"
WHAM_TOL="${WHAM_TOL:-1e-5}"
GMX_BIN="${GMX_BIN:-gmx}"
FORCE_RERUN="${FORCE_RERUN:-false}"

usage() {
    cat <<'EOF'
Usage: free-energy-analysis.sh [options]

Core options:
  --mode all|bar|wham|awh|summary
  --input-dir DIR
  --output-dir DIR
  --temperature K
  --series FILE              Time series for block averaging

BAR/FEP:
  --bar-inputs "a.xvg b.xvg"    Explicit BAR/FEP inputs
  --bar-pattern GLOB             Auto-detect BAR inputs (e.g. 'lambda_*/dhdl*.xvg')

WHAM/PMF:
  --wham-tpr-list FILE
  --wham-pullf-list FILE
  --pmf FILE
  --hist FILE
  --bootstrap N

AWH:
  --awh-edr FILE
  --awh-log FILE
  --awh-pmf FILE

Behavior:
  --force-rerun true|false   Recompute even if output exists

Examples:
  bash scripts/analysis/free-energy-analysis.sh --mode all \
    --input-dir umbrella --wham-tpr-list umbrella/tpr_files.dat \
    --wham-pullf-list umbrella/pullf_files.dat

  bash scripts/analysis/free-energy-analysis.sh --mode bar \
    --bar-pattern 'freeenergy_results/lambda_*/dhdl*.xvg'
EOF
}

log() { echo "[$(date '+%F %T')] $*"; }
warn() { echo "[WARN] $*" >&2; }
die() { echo "[ERROR] $*" >&2; exit 1; }

have_cmd() { command -v "$1" >/dev/null 2>&1; }
need_file() { [[ -f "$1" ]] || die "File not found: $1"; }
abs_path() {
    python3 - <<'PY' "$1"
import os,sys
print(os.path.abspath(sys.argv[1]))
PY
}

# Minimal XVG numeric extractor.
series_stats() {
    local file="$1"
    local col="${2:-2}"
    awk -v c="$col" '
        $0 !~ /^[@#]/ && NF >= c {
            x=$c+0; n++; s+=x; ss+=x*x;
            if(n==1 || x<min) min=x;
            if(n==1 || x>max) max=x;
            vals[n]=x;
        }
        END {
            if(n==0){print "count=0"; exit}
            mean=s/n; var=(ss/n)-(mean*mean); if(var<0)var=0; std=sqrt(var);
            print "count=" n;
            printf("mean=%.6f\nmin=%.6f\nmax=%.6f\nstd=%.6f\nrange=%.6f\n", mean, min, max, std, max-min);
        }
    ' "$file"
}

block_average_stats() {
    local file="$1"
    local col="${2:-2}"
    local blocks="$3"
    awk -v c="$col" -v nb="$blocks" '
        $0 !~ /^[@#]/ && NF >= c {vals[++n]=$c+0}
        END {
            if(n<nb || n==0){print "blocks=0"; exit}
            bs=int(n/nb); if(bs<1){print "blocks=0"; exit}
            for(i=1;i<=nb;i++){
                start=(i-1)*bs+1; end=(i==nb?n:i*bs);
                sum=0; cnt=0;
                for(j=start;j<=end;j++){sum+=vals[j]; cnt++}
                m[i]=sum/cnt; ms+=m[i]; mss+=m[i]*m[i];
            }
            mean=ms/nb; var=(mss/nb)-(mean*mean); if(var<0)var=0;
            stderr=sqrt(var/nb);
            printf("blocks=%d\nblock_size=%d\nblock_mean=%.6f\nblock_stderr=%.6f\n", nb, bs, mean, stderr);
        }
    ' "$file"
}

parse_key() {
    local file="$1"
    local key="$2"
    awk -F= -v k="$key" '$1==k {print $2}' "$file" | tail -1
}

find_first_existing() {
    for p in "$@"; do
        [[ -n "$p" && -f "$p" ]] && { echo "$p"; return 0; }
    done
    return 1
}

collect_glob() {
    local pattern="$1"
    python3 - <<'PY' "$pattern"
import glob,sys
for path in sorted(glob.glob(sys.argv[1])):
    print(path)
PY
}

run_bar_analysis() {
    local method_dir="$OUTPUT_DIR/bar"
    mkdir -p "$method_dir"
    local inputs=()
    local bar_out="$method_dir/bar.xvg"
    local bar_log="$method_dir/bar.log"
    local bar_txt="$method_dir/bar_summary.txt"

    if [[ -n "$BAR_INPUTS" ]]; then
        # shellcheck disable=SC2206
        inputs=($BAR_INPUTS)
    elif [[ -n "$BAR_PATTERN" ]]; then
        mapfile -t inputs < <(collect_glob "$BAR_PATTERN")
    else
        mapfile -t inputs < <(cd "$INPUT_DIR" && find . -type f \( -name 'dhdl*.xvg' -o -name 'bar*.xvg' -o -name 'fe*.xvg' \) | sort | sed 's#^./##')
        for i in "${!inputs[@]}"; do inputs[$i]="$INPUT_DIR/${inputs[$i]}"; done
    fi

    if [[ ${#inputs[@]} -lt 2 ]]; then
        warn "BAR/FEP inputs not sufficient; skip BAR analysis"
        return 0
    fi

    printf '%s
' "${inputs[@]}" > "$method_dir/inputs.list"

    if have_cmd "$GMX_BIN" && { [[ ! -f "$bar_out" ]] || [[ "$FORCE_RERUN" == "true" ]]; }; then
        log "Running gmx bar on ${#inputs[@]} files"
        "$GMX_BIN" bar -f "${inputs[@]}" -o "$bar_out" -oi "$method_dir/barint.xvg" > "$bar_log" 2>&1 || warn "gmx bar failed; fallback to existing files only"
    fi

    local source_file
    source_file=$(find_first_existing "$bar_out" "$INPUT_DIR/analysis/bar.xvg" "$INPUT_DIR/bar.xvg") || true
    if [[ -n "${source_file:-}" ]]; then
        cp "$source_file" "$method_dir/bar_source.xvg"
        series_stats "$source_file" 2 > "$method_dir/bar_stats.env"
    else
        echo "count=0" > "$method_dir/bar_stats.env"
    fi

    local total="NA" err="NA"
    if [[ -f "$bar_log" ]]; then
        total=$(awk '/[Tt]otal/ && /[Dd]elta|[Tt]otal/ && /[Gg]/ {
            for(i=1;i<=NF;i++) if($i ~ /^-?[0-9.]+$/){vals[++n]=$i}
        } END{if(n>=1) print vals[1]}' "$bar_log")
        err=$(awk '/\+\/-|\+-/ {
            for(i=1;i<=NF;i++) if($i ~ /^-?[0-9.]+$/){vals[++n]=$i}
        } END{if(n>=2) print vals[2]}' "$bar_log")
    fi
    if [[ "$total" == "NA" || -z "$total" ]]; then
        total=$(awk '$0 !~ /^[@#]/ && NF>=2 {v=$2} END{if(v!="") printf "%.4f", v}' "$method_dir/bar_source.xvg" 2>/dev/null || true)
        [[ -z "$total" ]] && total="NA"
    fi
    if [[ "$err" == "NA" || -z "$err" ]]; then
        err=$(awk '$0 !~ /^[@#]/ && NF>=3 {v=$3} END{if(v!="") printf "%.4f", v}' "$method_dir/bar_source.xvg" 2>/dev/null || true)
        [[ -z "$err" ]] && err="NA"
    fi

    cat > "$bar_txt" <<EOF
method=BAR/FEP
input_count=${#inputs[@]}
delta_g=$total
error=$err
EOF
}

run_wham_analysis() {
    local method_dir="$OUTPUT_DIR/wham"
    mkdir -p "$method_dir"
    local wham_log="$method_dir/wham.log"
    local pmf_out="$method_dir/pmf.xvg"
    local hist_out="$method_dir/hist.xvg"
    local bserr_out="$method_dir/bsres.xvg"
    local summary="$method_dir/wham_summary.txt"

    if [[ -z "$WHAM_TPR_LIST" ]]; then
        WHAM_TPR_LIST=$(find_first_existing "$INPUT_DIR/tpr_files.dat" "$INPUT_DIR/tpr_files.txt" "$INPUT_DIR/tpr-files.dat" || true)
    fi
    if [[ -z "$WHAM_PULLF_LIST" ]]; then
        WHAM_PULLF_LIST=$(find_first_existing "$INPUT_DIR/pullf_files.dat" "$INPUT_DIR/pullf-files.dat" "$INPUT_DIR/pullf_files.txt" || true)
    fi
    if [[ -z "$PMF_FILE" ]]; then
        PMF_FILE=$(find_first_existing "$INPUT_DIR/pmf.xvg" "$INPUT_DIR/analysis/pmf.xvg" "$pmf_out" || true)
    fi
    if [[ -z "$HIST_FILE" ]]; then
        HIST_FILE=$(find_first_existing "$INPUT_DIR/hist.xvg" "$INPUT_DIR/analysis/hist.xvg" "$hist_out" || true)
    fi

    if [[ -n "$WHAM_TPR_LIST" && -n "$WHAM_PULLF_LIST" ]] && have_cmd "$GMX_BIN" && { [[ ! -f "$pmf_out" ]] || [[ "$FORCE_RERUN" == "true" ]]; }; then
        log "Running gmx wham"
        "$GMX_BIN" wham -it "$WHAM_TPR_LIST" -if "$WHAM_PULLF_LIST" -o "$pmf_out" -hist "$hist_out" -bsres "$bserr_out" -nBootstrap "$BOOTSTRAP_SAMPLES" -tol "$WHAM_TOL" > "$wham_log" 2>&1 || warn "gmx wham failed; fallback to existing PMF"
    fi

    PMF_FILE=$(find_first_existing "$pmf_out" "$PMF_FILE" || true)
    HIST_FILE=$(find_first_existing "$hist_out" "$HIST_FILE" || true)
    [[ -n "$PMF_FILE" ]] && cp "$PMF_FILE" "$method_dir/pmf_source.xvg"
    [[ -n "$HIST_FILE" ]] && cp "$HIST_FILE" "$method_dir/hist_source.xvg"

    if [[ -n "$PMF_FILE" && -f "$PMF_FILE" ]]; then
        series_stats "$PMF_FILE" 2 > "$method_dir/pmf_stats.env"
        awk '
            $0 !~ /^[@#]/ && NF>=2 {x[++n]=$1+0; y[n]=$2+0}
            END {
                if(n<3){print "baseline_drift=NA\nroughness=NA\nbarriers=NA"; exit}
                baseline = y[n]-y[1];
                turns=0;
                for(i=2;i<n;i++){
                    d1=y[i]-y[i-1]; d2=y[i+1]-y[i];
                    if((d1>0 && d2<0) || (d1<0 && d2>0)) turns++;
                }
                printf("baseline_drift=%.6f\nroughness=%d\nbarriers=%d\n", baseline, turns/(n>50?n/50:1), turns)
            }
        ' "$PMF_FILE" > "$method_dir/pmf_quality.env"
    else
        echo "count=0" > "$method_dir/pmf_stats.env"
        echo -e "baseline_drift=NA\nroughness=NA\nbarriers=NA" > "$method_dir/pmf_quality.env"
    fi

    if [[ -n "$HIST_FILE" && -f "$HIST_FILE" ]]; then
        awk '
            $0 !~ /^[@#]/ && NF>=2 {
                total++; occupied=0;
                for(i=2;i<=NF;i++) if(($i+0)>0) occupied++;
                if(occupied>0) nonzero++;
                if(occupied>1) overlap++;
                occsum+=occupied;
            }
            END {
                if(total==0){print "hist_total=0"; exit}
                printf("hist_total=%d\nhist_nonzero_ratio=%.4f\nhist_overlap_ratio=%.4f\nmean_occupied_bins=%.4f\n", total, nonzero/total, overlap/total, occsum/total)
            }
        ' "$HIST_FILE" > "$method_dir/hist_stats.env"
    else
        echo "hist_total=0" > "$method_dir/hist_stats.env"
    fi

    local pmf_err="NA"
    if [[ -f "$bserr_out" ]]; then
        awk '$0 !~ /^[@#]/ && NF>=3 {s+=$3; n++} END{if(n>0) printf "%.4f", s/n; else print "NA"}' "$bserr_out" > "$method_dir/bootstrap_mean.err"
        pmf_err=$(cat "$method_dir/bootstrap_mean.err")
    elif [[ -n "$PMF_FILE" ]]; then
        pmf_err=$(awk '$0 !~ /^[@#]/ && NF>=3 {s+=$3; n++} END{if(n>0) printf "%.4f", s/n; else print "NA"}' "$PMF_FILE")
    fi

    local converged="unknown"
    if [[ -f "$wham_log" ]]; then
        if grep -qi "did not converge" "$wham_log"; then converged="no"; fi
        if grep -qi "converged" "$wham_log"; then converged="yes"; fi
    fi

    cat > "$summary" <<EOF
method=WHAM/PMF
pmf_file=${PMF_FILE:-NA}
hist_file=${HIST_FILE:-NA}
bootstrap_error=$pmf_err
converged=$converged
EOF
}

run_awh_analysis() {
    local method_dir="$OUTPUT_DIR/awh"
    mkdir -p "$method_dir"
    local summary="$method_dir/awh_summary.txt"
    local awh_log_local="$method_dir/awh_extract.log"

    if [[ -z "$AWH_EDR" ]]; then
        AWH_EDR=$(find_first_existing "$INPUT_DIR/md.edr" "$INPUT_DIR/awh.edr" || true)
    fi
    if [[ -z "$AWH_LOG" ]]; then
        AWH_LOG=$(find_first_existing "$INPUT_DIR/md.log" "$INPUT_DIR/awh.log" || true)
    fi
    if [[ -z "$AWH_PMF" ]]; then
        AWH_PMF=$(find_first_existing "$INPUT_DIR/awh_pmf.xvg" "$INPUT_DIR/pmf.xvg" "$INPUT_DIR/awh.xvg" || true)
    fi

    if [[ -n "$AWH_EDR" ]] && have_cmd "$GMX_BIN" && { [[ ! -f "$method_dir/awh_pmf.xvg" ]] || [[ "$FORCE_RERUN" == "true" ]]; }; then
        log "Trying gmx awh"
        "$GMX_BIN" awh -f "$AWH_EDR" -o "$method_dir/awh_pmf.xvg" -more > "$awh_log_local" 2>&1 || warn "gmx awh failed; using existing AWH files/logs only"
    fi

    AWH_PMF=$(find_first_existing "$method_dir/awh_pmf.xvg" "$AWH_PMF" || true)
    [[ -n "$AWH_PMF" && -f "$AWH_PMF" ]] && cp "$AWH_PMF" "$method_dir/awh_source.xvg"
    if [[ -n "$AWH_PMF" && -f "$AWH_PMF" ]]; then
        series_stats "$AWH_PMF" 2 > "$method_dir/awh_stats.env"
    else
        echo "count=0" > "$method_dir/awh_stats.env"
    fi

    local stage="unknown"
    local note="Inspect target distribution, visit counts, and bias update stability."
    if [[ -n "$AWH_LOG" && -f "$AWH_LOG" ]]; then
        if grep -Eqi 'equilibrat|initial stage|exploration' "$AWH_LOG"; then
            stage="exploration"
            note="Still in exploration; do not over-interpret PMF yet."
        fi
        if grep -Eqi 'converged|flat target|covered' "$AWH_LOG"; then
            stage="near-converged"
            note="Target coverage looks reasonable; compare last thirds of PMF before publishing."
        fi
    fi

    cat > "$summary" <<EOF
method=AWH
awh_pmf=${AWH_PMF:-NA}
stage=$stage
recommendation=$note
EOF
}

build_master_report() {
    local report="$OUTPUT_DIR/$REPORT_NAME"
    mkdir -p "$OUTPUT_DIR"

    local bar_delta="NA" bar_err="NA" bar_inputs="0"
    [[ -f "$OUTPUT_DIR/bar/bar_summary.txt" ]] && {
        bar_delta=$(awk -F= '$1=="delta_g"{print $2}' "$OUTPUT_DIR/bar/bar_summary.txt")
        bar_err=$(awk -F= '$1=="error"{print $2}' "$OUTPUT_DIR/bar/bar_summary.txt")
        bar_inputs=$(awk -F= '$1=="input_count"{print $2}' "$OUTPUT_DIR/bar/bar_summary.txt")
    }

    local pmf_range="NA" pmf_err="NA" overlap="NA" drift="NA" roughness="NA" wham_conv="unknown"
    [[ -f "$OUTPUT_DIR/wham/pmf_stats.env" ]] && pmf_range=$(parse_key "$OUTPUT_DIR/wham/pmf_stats.env" range)
    [[ -f "$OUTPUT_DIR/wham/wham_summary.txt" ]] && {
        pmf_err=$(awk -F= '$1=="bootstrap_error"{print $2}' "$OUTPUT_DIR/wham/wham_summary.txt")
        wham_conv=$(awk -F= '$1=="converged"{print $2}' "$OUTPUT_DIR/wham/wham_summary.txt")
    }
    [[ -f "$OUTPUT_DIR/wham/hist_stats.env" ]] && overlap=$(parse_key "$OUTPUT_DIR/wham/hist_stats.env" hist_overlap_ratio)
    [[ -f "$OUTPUT_DIR/wham/pmf_quality.env" ]] && {
        drift=$(parse_key "$OUTPUT_DIR/wham/pmf_quality.env" baseline_drift)
        roughness=$(parse_key "$OUTPUT_DIR/wham/pmf_quality.env" roughness)
    }

    local awh_stage="NA" awh_rec="NA"
    [[ -f "$OUTPUT_DIR/awh/awh_summary.txt" ]] && {
        awh_stage=$(awk -F= '$1=="stage"{print $2}' "$OUTPUT_DIR/awh/awh_summary.txt")
        awh_rec=$(awk -F= '$1=="recommendation"{sub($1"=",""); print}' "$OUTPUT_DIR/awh/awh_summary.txt")
    }

    local series_block_mean="NA" series_block_err="NA"
    if [[ -n "$SERIES_FILE" && -f "$SERIES_FILE" ]]; then
        block_average_stats "$SERIES_FILE" 2 "$BLOCK_COUNT" > "$OUTPUT_DIR/block_average.env"
        series_block_mean=$(parse_key "$OUTPUT_DIR/block_average.env" block_mean)
        series_block_err=$(parse_key "$OUTPUT_DIR/block_average.env" block_stderr)
    fi

    local overall="usable"
    local judge=()
    if [[ "$overlap" != "NA" ]]; then
        awk -v x="$overlap" 'BEGIN{exit !(x+0<0.30)}' && { overall="needs-more-sampling"; judge+=("window overlap low"); }
    fi
    if [[ "$drift" != "NA" ]]; then
        awk -v x="$drift" 'BEGIN{ax=(x<0?-x:x); exit !(ax>5.0)}' && { overall="needs-more-sampling"; judge+=("PMF baseline drift > 5 kJ/mol"); }
    fi
    if [[ "$roughness" != "NA" ]]; then
        awk -v x="$roughness" 'BEGIN{exit !(x+0>8)}' && judge+=("PMF is rough/noisy")
    fi
    if [[ "$wham_conv" == "no" ]]; then overall="needs-more-sampling"; judge+=("WHAM not converged"); fi
    if [[ ${#judge[@]} -eq 0 ]]; then judge+=("no major red flags detected from available files"); fi

    cat > "$report" <<EOF
# Free Energy Analysis Report

## Run Summary

- Mode: $MODE
- Input directory: $(abs_path "$INPUT_DIR")
- Output directory: $(abs_path "$OUTPUT_DIR")
- Temperature: $TEMPERATURE K
- Overall assessment: **$overall**

## 1. BAR / FEP

- Input files: $bar_inputs
- Delta G: $bar_delta kJ/mol
- Reported error: $bar_err kJ/mol
- Interpretation: Prefer BAR only when adjacent lambda states have sufficient overlap and per-window sampling is balanced.

## 2. WHAM / PMF

- PMF range: $pmf_range kJ/mol
- Bootstrap / mean PMF error: $pmf_err kJ/mol
- Histogram overlap ratio: $overlap
- WHAM convergence: $wham_conv
- Baseline drift: $drift kJ/mol
- Roughness indicator: $roughness

## 3. AWH

- Stage: $awh_stage
- Recommendation: $awh_rec

## 4. Error Estimation

- Bootstrap samples requested: $BOOTSTRAP_SAMPLES
- Block average mean: $series_block_mean
- Block average stderr: $series_block_err
- Note: Block averaging is only computed when \`--series\` is provided.

## 5. Quality Checks

$(for item in "${judge[@]}"; do echo "- $item"; done)

## 6. Cross-Method Reading

- If BAR and WHAM/AWH agree within combined uncertainty, the free energy picture is internally consistent.
- If BAR disagrees with PMF shape, first check lambda overlap, restraint definitions, and reaction coordinate hysteresis.
- If PMF has large end-point drift or poor overlap, extend edge windows and reduce window spacing before interpreting barriers.
- For AWH, only trust final PMF after target coverage stabilizes and late-stage segments give similar profiles.

## 7. Output Files

- \`bar/\` : BAR/FEP summaries and copied source files
- \`wham/\` : PMF, histogram, bootstrap outputs, quality stats
- \`awh/\` : AWH extraction and recommendation notes
- \`block_average.env\` : block averaging summary (if series supplied)

EOF

    log "Master report generated: $report"
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --mode) MODE="$2"; shift 2 ;;
            --input-dir) INPUT_DIR="$2"; shift 2 ;;
            --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
            --report-name) REPORT_NAME="$2"; shift 2 ;;
            --bar-inputs) BAR_INPUTS="$2"; shift 2 ;;
            --bar-pattern) BAR_PATTERN="$2"; shift 2 ;;
            --wham-tpr-list) WHAM_TPR_LIST="$2"; shift 2 ;;
            --wham-pullf-list) WHAM_PULLF_LIST="$2"; shift 2 ;;
            --pmf) PMF_FILE="$2"; shift 2 ;;
            --hist) HIST_FILE="$2"; shift 2 ;;
            --awh-edr) AWH_EDR="$2"; shift 2 ;;
            --awh-log) AWH_LOG="$2"; shift 2 ;;
            --awh-pmf) AWH_PMF="$2"; shift 2 ;;
            --series) SERIES_FILE="$2"; shift 2 ;;
            --temperature) TEMPERATURE="$2"; shift 2 ;;
            --bootstrap) BOOTSTRAP_SAMPLES="$2"; shift 2 ;;
            --blocks) BLOCK_COUNT="$2"; shift 2 ;;
            --force-rerun) FORCE_RERUN="$2"; shift 2 ;;
            -h|--help) usage; exit 0 ;;
            *) die "Unknown option: $1" ;;
        esac
    done
}

main() {
    parse_args "$@"
    mkdir -p "$OUTPUT_DIR"

    case "$MODE" in
        all)
            run_bar_analysis
            run_wham_analysis
            run_awh_analysis
            ;;
        bar) run_bar_analysis ;;
        wham) run_wham_analysis ;;
        awh) run_awh_analysis ;;
        summary) : ;;
        *) die "Unsupported mode: $MODE" ;;
    esac

    build_master_report
    log "Free energy analysis completed"
}

main "$@"
