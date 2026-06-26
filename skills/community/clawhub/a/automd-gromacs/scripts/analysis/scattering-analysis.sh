#!/bin/bash
# scattering-analysis - SAXS/SANS and experiment-comparison workflow
# Supports gmx saxs/gmx sans/gmx scattering plus report-ready summaries.

set -euo pipefail

show_help() {
    cat << 'EOF'
scattering-analysis - SAXS/SANS/Experiment Comparison Analysis

USAGE:
  scattering-analysis -s md.tpr -f md.xtc [OPTIONS]
  scattering-analysis --curve simulated.dat --exp experiment.dat [OPTIONS]

MODES:
  saxs       - Calculate SAXS with gmx saxs
  sans       - Calculate SANS with gmx sans (or organize existing data)
  compare    - Compare simulated and experimental curves
  interpret  - Basic Guinier/Kratky interpretation from one curve
  report     - Generate report from existing outputs
  all        - Run calculation + comparison + interpretation + report

INPUT OPTIONS:
  -s FILE              TPR/structure file for GROMACS calculation
  -f FILE              Trajectory file for GROMACS calculation
  -n FILE              Index file (optional)
  -o DIR               Output directory (default: scattering-analysis)
  --mode MODE          Mode: saxs/sans/compare/interpret/report/all (default: all)
  --group NAME         Selection group (default: System)
  --curve FILE         Simulated scattering curve (2-4 columns: q I [err] [Iq2])
  --exp FILE           Experimental curve (2-3 columns: q I [err])
  --sans FILE          Existing SANS/scattering curve to organize
  --qmin VALUE         q minimum (1/nm, default: auto)
  --qmax VALUE         q maximum (1/nm, default: auto)
  --qpoints N          Number of q points for generated grid (default: 200)
  --contrast VALUE     Contrast factor for SANS notes/report (default: auto)
  --buffer-density V   Buffer density hint for preparation notes (default: auto)
  --skip N             Skip frames (default: 1)
  -b TIME              Begin time in ps
  -e TIME              End time in ps
  --label TEXT         Dataset label (default: auto)
  -h, --help           Show this help

EXAMPLES:
  # SAXS from MD and compare with experiment
  scattering-analysis -s md.tpr -f md.xtc --exp exp_saxs.dat --mode all

  # Only compare existing simulated vs experimental curves
  scattering-analysis --curve calc_saxs.xvg --exp exp_saxs.dat --mode compare

  # Organize SANS result and produce interpretation/report
  scattering-analysis --sans sans_curve.dat --exp exp_sans.dat --mode all

  # Interpret an existing curve without GROMACS calculation
  scattering-analysis --curve calc_saxs.xvg --mode interpret

OUTPUT:
  curves/                      Cleaned and normalized curve files
  compare/curve_comparison.tsv Interpolated simulated/experimental comparison
  compare/deviation_summary.txt Fit error summary
  interpret/guinier_summary.txt Guinier region estimate
  interpret/kratky_summary.txt  Kratky peak/tail description
  figures/scattering_plot.png   Plot when python3+matplotlib is available
  export/scattering_export.tsv  Publication/automd-viz friendly export
  export/scattering_export.json Machine-readable summary
  SCATTERING_REPORT.md          Markdown report

EXPERIMENT NOTES:
  - SAXS useful q range: 0.1-3.0 1/nm for global shape, 1-10 1/nm for finer features.
  - Guinier region should satisfy q*Rg < 1.3 for compact systems.
  - Dimensionless Kratky peak near sqrt(3), 3 indicates folded globular behavior.
  - For SANS, contrast matching and H/D composition dominate interpretability.
EOF
}

TPR=""
TRJ=""
NDX=""
OUTDIR="scattering-analysis"
MODE="all"
GROUP="System"
CURVE_FILE=""
EXP_FILE=""
SANS_FILE=""
QMIN=""
QMAX=""
QPOINTS=200
CONTRAST="auto"
BUFFER_DENSITY="auto"
SKIP=1
BEGIN=""
END=""
LABEL="auto"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) show_help; exit 0 ;;
        -s) TPR="$2"; shift 2 ;;
        -f) TRJ="$2"; shift 2 ;;
        -n) NDX="$2"; shift 2 ;;
        -o) OUTDIR="$2"; shift 2 ;;
        --mode) MODE="$2"; shift 2 ;;
        --group) GROUP="$2"; shift 2 ;;
        --curve) CURVE_FILE="$2"; shift 2 ;;
        --exp) EXP_FILE="$2"; shift 2 ;;
        --sans) SANS_FILE="$2"; shift 2 ;;
        --qmin) QMIN="$2"; shift 2 ;;
        --qmax) QMAX="$2"; shift 2 ;;
        --qpoints) QPOINTS="$2"; shift 2 ;;
        --contrast) CONTRAST="$2"; shift 2 ;;
        --buffer-density) BUFFER_DENSITY="$2"; shift 2 ;;
        --skip) SKIP="$2"; shift 2 ;;
        -b) BEGIN="$2"; shift 2 ;;
        -e) END="$2"; shift 2 ;;
        --label) LABEL="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; show_help; exit 1 ;;
    esac
done

log() { echo "[$(date '+%H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }
warn() { echo "[WARN] $*" >&2; }
check_file() { [[ -f "$1" ]] || error "File not found: $1"; }

need_calc=false
[[ "$MODE" == "saxs" || "$MODE" == "sans" || "$MODE" == "all" ]] && need_calc=true
if $need_calc; then
    [[ -z "$TPR" ]] && error "-s <tpr> required for calculation mode"
    [[ -z "$TRJ" ]] && error "-f <trajectory> required for calculation mode"
    check_file "$TPR"
    check_file "$TRJ"
fi
[[ -n "$NDX" ]] && check_file "$NDX"
[[ -n "$CURVE_FILE" ]] && check_file "$CURVE_FILE"
[[ -n "$EXP_FILE" ]] && check_file "$EXP_FILE"
[[ -n "$SANS_FILE" ]] && check_file "$SANS_FILE"

mkdir -p "$OUTDIR" "$OUTDIR/curves" "$OUTDIR/compare" "$OUTDIR/interpret" "$OUTDIR/figures" "$OUTDIR/export" "$OUTDIR/logs"

if [[ "$LABEL" == "auto" ]]; then
    LABEL="$(basename "${EXP_FILE:-${CURVE_FILE:-${SANS_FILE:-scattering}}}" | sed 's/\.[^.]*$//')"
fi

TIME_ARGS=""
[[ -n "$BEGIN" ]] && TIME_ARGS="$TIME_ARGS -b $BEGIN"
[[ -n "$END" ]] && TIME_ARGS="$TIME_ARGS -e $END"
[[ "$SKIP" != "1" ]] && TIME_ARGS="$TIME_ARGS -dt $SKIP"

normalize_curve() {
    local input="$1"
    local output="$2"
    python3 - "$input" "$output" << 'PY'
import sys, math
src, dst = sys.argv[1:3]
rows = []
with open(src, 'r', encoding='utf-8', errors='ignore') as fh:
    for line in fh:
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('@'):
            continue
        parts = s.replace(',', ' ').split()
        vals = []
        for token in parts:
            try:
                vals.append(float(token))
            except ValueError:
                pass
        if len(vals) < 2:
            continue
        q = vals[0]
        inten = vals[1]
        err = vals[2] if len(vals) >= 3 else float('nan')
        rows.append((q, inten, err))
rows.sort(key=lambda x: x[0])
if not rows:
    raise SystemExit('no numeric rows found')
with open(dst, 'w', encoding='utf-8') as out:
    out.write('# q intensity error\n')
    for q, inten, err in rows:
        err_txt = 'nan' if math.isnan(err) else f'{err:.8g}'
        out.write(f'{q:.8g}\t{inten:.8g}\t{err_txt}\n')
PY
}

write_prep_notes() {
    cat > "$OUTDIR/compare/input_preparation_notes.md" << EOF
# Scattering Input Preparation Notes

- Recommended q-range: global shape 0.1-3.0 1/nm; intermediate features 3-10 1/nm.
- Use identical q grid for simulation and experiment when possible to reduce interpolation bias.
- SAXS: buffer subtraction, concentration normalization, and low-q aggregation check are mandatory.
- SANS: record D2O/H2O fraction, solvent match point, isotope labeling, and contrast factor.
- Suggested contrast factor: ${CONTRAST}
- Buffer density hint: ${BUFFER_DENSITY}
- Preferred experimental columns: q intensity error
- If experiment uses 1/A, convert to 1/nm by multiplying q by 10.
EOF
}

calc_saxs() {
    command -v gmx >/dev/null 2>&1 || error "ERROR-001: gmx not found for SAXS calculation"
    log "Running SAXS calculation with gmx saxs"
    local out="$OUTDIR/curves/saxs_raw.xvg"
    local cmd=(gmx saxs -s "$TPR" -f "$TRJ" -o "$out")
    [[ -n "$NDX" ]] && cmd+=( -n "$NDX" )
    [[ -n "$QMIN" ]] && cmd+=( -startq "$QMIN" )
    [[ -n "$QMAX" ]] && cmd+=( -endq "$QMAX" )
    [[ -n "$QPOINTS" ]] && cmd+=( -ng "$QPOINTS" )
    # Many GROMACS builds accept stdin group selection.
    printf '%s\n' "$GROUP" | "${cmd[@]}" $TIME_ARGS > "$OUTDIR/logs/saxs.log" 2>&1 || {
        warn "gmx saxs failed, see $OUTDIR/logs/saxs.log"
        return 1
    }
    normalize_curve "$out" "$OUTDIR/curves/saxs_curve.dat"
    CURVE_FILE="$OUTDIR/curves/saxs_curve.dat"
    echo "SAXS" > "$OUTDIR/curves/mode.txt"
}

calc_sans() {
    if [[ -n "$SANS_FILE" ]]; then
        log "Organizing existing SANS/scattering file"
        normalize_curve "$SANS_FILE" "$OUTDIR/curves/sans_curve.dat"
        CURVE_FILE="$OUTDIR/curves/sans_curve.dat"
        echo "SANS" > "$OUTDIR/curves/mode.txt"
        return 0
    fi
    command -v gmx >/dev/null 2>&1 || error "ERROR-001: gmx not found for SANS calculation"
    if gmx help commands 2>/dev/null | grep -q " sans\|^sans"; then
        log "Running SANS calculation with gmx sans"
        local out="$OUTDIR/curves/sans_raw.xvg"
        local cmd=(gmx sans -s "$TPR" -f "$TRJ" -o "$out")
        [[ -n "$NDX" ]] && cmd+=( -n "$NDX" )
        printf '%s\n' "$GROUP" | "${cmd[@]}" $TIME_ARGS > "$OUTDIR/logs/sans.log" 2>&1 || {
            warn "gmx sans failed, see $OUTDIR/logs/sans.log"
            return 1
        }
        normalize_curve "$out" "$OUTDIR/curves/sans_curve.dat"
        CURVE_FILE="$OUTDIR/curves/sans_curve.dat"
        echo "SANS" > "$OUTDIR/curves/mode.txt"
    elif gmx help commands 2>/dev/null | grep -q " scattering\|^scattering"; then
        log "gmx sans unavailable, using gmx scattering fallback"
        local out="$OUTDIR/curves/scattering_raw.xvg"
        local cmd=(gmx scattering -s "$TPR" -f "$TRJ" -o "$out")
        [[ -n "$NDX" ]] && cmd+=( -n "$NDX" )
        printf '%s\n' "$GROUP" | "${cmd[@]}" $TIME_ARGS > "$OUTDIR/logs/scattering.log" 2>&1 || {
            warn "gmx scattering failed, see $OUTDIR/logs/scattering.log"
            return 1
        }
        normalize_curve "$out" "$OUTDIR/curves/sans_curve.dat"
        CURVE_FILE="$OUTDIR/curves/sans_curve.dat"
        echo "SANS" > "$OUTDIR/curves/mode.txt"
    else
        error "ERROR-002: gmx sans/scattering not available; provide --sans existing_curve.dat"
    fi
}

prepare_existing_curve() {
    [[ -n "$CURVE_FILE" ]] || return 0
    normalize_curve "$CURVE_FILE" "$OUTDIR/curves/sim_curve.dat"
    CURVE_FILE="$OUTDIR/curves/sim_curve.dat"
    [[ ! -f "$OUTDIR/curves/mode.txt" ]] && echo "SIMULATION" > "$OUTDIR/curves/mode.txt"
}

prepare_experiment() {
    [[ -n "$EXP_FILE" ]] || return 0
    normalize_curve "$EXP_FILE" "$OUTDIR/curves/exp_curve.dat"
    EXP_FILE="$OUTDIR/curves/exp_curve.dat"
}

compare_curves() {
    [[ -n "$CURVE_FILE" ]] || error "ERROR-003: missing simulated curve for comparison"
    [[ -n "$EXP_FILE" ]] || error "ERROR-004: missing experimental curve for comparison"
    log "Comparing simulated and experimental curves"
    python3 - "$CURVE_FILE" "$EXP_FILE" "$OUTDIR/compare/curve_comparison.tsv" "$OUTDIR/compare/deviation_summary.txt" << 'PY'
import sys, math, statistics
sim_path, exp_path, out_tsv, out_txt = sys.argv[1:5]

def read_curve(path):
    q, i, e = [], [], []
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not line.strip() or line.startswith('#'):
                continue
            parts = line.split()
            q.append(float(parts[0]))
            i.append(float(parts[1]))
            try:
                err = float(parts[2])
            except Exception:
                err = float('nan')
            e.append(err)
    return q, i, e

def interp(x, xp, fp):
    if x < xp[0] or x > xp[-1]:
        return None
    lo = 0
    hi = len(xp) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xp[mid] <= x:
            lo = mid
        else:
            hi = mid
    x0, x1 = xp[lo], xp[hi]
    y0, y1 = fp[lo], fp[hi]
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

q_sim, i_sim, _ = read_curve(sim_path)
q_exp, i_exp, e_exp = read_curve(exp_path)
if len(q_sim) < 3 or len(q_exp) < 3:
    raise SystemExit('curves too short for comparison')
common = []
for q, ie, ee in zip(q_exp, i_exp, e_exp):
    isim = interp(q, q_sim, i_sim)
    if isim is None:
        continue
    common.append((q, isim, ie, ee))
if len(common) < 5:
    raise SystemExit('insufficient q overlap between curves')
scale_num = sum(ie * isim for _, isim, ie, _ in common)
scale_den = sum(isim * isim for _, isim, _, _ in common)
scale = scale_num / scale_den if scale_den else 1.0
rows = []
res = []
chi_terms = []
for q, isim, ie, ee in common:
    scaled = isim * scale
    delta = scaled - ie
    rel = delta / ie if ie else float('nan')
    rows.append((q, scaled, ie, delta, rel, ee))
    res.append(delta)
    if not math.isnan(ee) and ee > 0:
        chi_terms.append((delta / ee) ** 2)
rmse = math.sqrt(sum(x*x for x in res) / len(res))
mae = sum(abs(x) for x in res) / len(res)
mean_exp = sum(r[2] for r in rows) / len(rows)
rmsre = math.sqrt(sum((r[4]**2) for r in rows if not math.isnan(r[4])) / len(rows))
chi2 = sum(chi_terms) / len(chi_terms) if chi_terms else float('nan')
worst = max(rows, key=lambda r: abs(r[3]))
low = [r for r in rows if r[0] <= rows[0][0] + (rows[-1][0] - rows[0][0]) / 3.0]
mid = [r for r in rows if rows[0][0] + (rows[-1][0] - rows[0][0]) / 3.0 < r[0] <= rows[0][0] + 2*(rows[-1][0] - rows[0][0]) / 3.0]
high = [r for r in rows if r[0] > rows[0][0] + 2*(rows[-1][0] - rows[0][0]) / 3.0]

def band_mean(vals):
    return sum(abs(r[4]) for r in vals if not math.isnan(r[4])) / max(1, len(vals))
with open(out_tsv, 'w', encoding='utf-8') as out:
    out.write('q\tsim_scaled\texperimental\tdelta\trelative_delta\terror\n')
    for row in rows:
        out.write('\t'.join(f'{x:.8g}' if isinstance(x, float) and not math.isnan(x) else 'nan' for x in row) + '\n')
with open(out_txt, 'w', encoding='utf-8') as out:
    out.write('Curve comparison summary\n')
    out.write('========================\n')
    out.write(f'Points used: {len(rows)}\n')
    out.write(f'Scale factor applied to simulation: {scale:.6g}\n')
    out.write(f'RMSE: {rmse:.6g}\n')
    out.write(f'MAE: {mae:.6g}\n')
    out.write(f'RMS relative error: {rmsre:.6g}\n')
    out.write(f'Reduced chi-like score: {chi2:.6g}\n' if not math.isnan(chi2) else 'Reduced chi-like score: unavailable (missing experimental errors)\n')
    out.write(f'Worst mismatch at q={worst[0]:.6g}: delta={worst[3]:.6g}, rel={worst[4]:.6g}\n')
    out.write(f'Low-q mean |relative delta|: {band_mean(low):.6g}\n')
    out.write(f'Mid-q mean |relative delta|: {band_mean(mid):.6g}\n')
    out.write(f'High-q mean |relative delta|: {band_mean(high):.6g}\n')
    out.write('\nBias interpretation:\n')
    if band_mean(low) > band_mean(high) * 1.2:
        out.write('- Low-q mismatch dominates: check global size, aggregation, interparticle effects, or box/solvent subtraction.\n')
    if band_mean(high) > band_mean(low) * 1.2:
        out.write('- High-q mismatch dominates: check local packing, hydration layer, force field, or atom form factors.\n')
    if abs(worst[4]) < 0.1 if not math.isnan(worst[4]) else False:
        out.write('- Overall agreement is good; deviations are within ~10% at the worst sampled q point.\n')
PY
}

interpret_curve() {
    local src="${CURVE_FILE:-$EXP_FILE}"
    [[ -n "$src" ]] || error "ERROR-005: no curve available for interpretation"
    log "Running Guinier/Kratky interpretation"
    python3 - "$src" "$OUTDIR/interpret/guinier_summary.txt" "$OUTDIR/interpret/kratky_summary.txt" "$OUTDIR/export/scattering_export.json" << 'PY'
import sys, math, json
curve_path, guinier_out, kratky_out, json_out = sys.argv[1:5]
q, I = [], []
with open(curve_path, 'r', encoding='utf-8') as fh:
    for line in fh:
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split()
        q.append(float(parts[0]))
        I.append(float(parts[1]))
if len(q) < 8:
    raise SystemExit('not enough points for interpretation')
# Low-q points for Guinier fit.
q2 = [x*x for x in q]
lnI = [math.log(max(y, 1e-300)) for y in I]
window = max(5, min(12, len(q)//3))
best = None
for start in range(0, max(1, len(q)//2 - window + 1)):
    xs = q2[start:start+window]
    ys = lnI[start:start+window]
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))
    denom = n*sxx - sx*sx
    if denom == 0:
        continue
    slope = (n*sxy - sx*sy)/denom
    intercept = (sy - slope*sx)/n
    yhat = [intercept + slope*x for x in xs]
    ss_res = sum((a-b)**2 for a, b in zip(ys, yhat))
    ss_tot = sum((y - sy/n)**2 for y in ys) or 1.0
    r2 = 1.0 - ss_res/ss_tot
    if slope >= 0:
        continue
    rg = math.sqrt(max(0.0, -3.0*slope))
    qrg_max = max(math.sqrt(v) for v in xs) * rg
    score = r2 - abs(qrg_max - 1.0) * 0.05
    if best is None or score > best['score']:
        best = dict(start=start, stop=start+window, slope=slope, intercept=intercept, r2=r2, rg=rg, I0=math.exp(intercept), qrg_max=qrg_max, score=score)
if best is None:
    raise SystemExit('Guinier fit failed')
with open(guinier_out, 'w', encoding='utf-8') as out:
    out.write('Guinier summary\n')
    out.write('===============\n')
    out.write(f'Estimated Rg: {best["rg"]:.6g} nm\n')
    out.write(f'Estimated I(0): {best["I0"]:.6g}\n')
    out.write(f'Fit q window: {q[best["start"]]:.6g} to {q[best["stop"]-1]:.6g} 1/nm\n')
    out.write(f'Fit R^2: {best["r2"]:.6g}\n')
    out.write(f'Max qRg in fit window: {best["qrg_max"]:.6g}\n')
    if best['qrg_max'] <= 1.3:
        out.write('- Guinier criterion satisfied (qRg <= 1.3).\n')
    else:
        out.write('- Guinier criterion may be violated; use smaller low-q range or inspect aggregation/interparticle effects.\n')
# Kratky: dimensionless-ish proxy from q^2 I(q), using estimated Rg and I0.
xs = [qq * best['rg'] for qq in q]
ys = [(qq*best['rg'])**2 * ii / best['I0'] for qq, ii in zip(q, I)]
peak_idx = max(range(len(ys)), key=lambda i: ys[i])
peak_x, peak_y = xs[peak_idx], ys[peak_idx]
tail = sum(ys[-min(5, len(ys)):]) / min(5, len(ys))
with open(kratky_out, 'w', encoding='utf-8') as out:
    out.write('Kratky summary\n')
    out.write('==============\n')
    out.write(f'Peak at qRg = {peak_x:.6g}\n')
    out.write(f'Peak height = {peak_y:.6g}\n')
    out.write(f'High-q tail mean = {tail:.6g}\n')
    if abs(peak_x - math.sqrt(3)) < 0.6 and abs(peak_y - 3.0) < 1.0:
        out.write('- Consistent with compact/folded globular behavior.\n')
    elif tail > peak_y * 0.6:
        out.write('- Broad high-q tail suggests flexibility, disorder, or unresolved local heterogeneity.\n')
    else:
        out.write('- Intermediate Kratky behavior; inspect ensemble heterogeneity and solvent model.\n')
with open(json_out, 'w', encoding='utf-8') as out:
    json.dump({
        'rg_nm': best['rg'],
        'i0': best['I0'],
        'guinier_r2': best['r2'],
        'guinier_qrg_max': best['qrg_max'],
        'kratky_peak_qrg': peak_x,
        'kratky_peak_height': peak_y,
        'kratky_tail_mean': tail
    }, out, indent=2)
PY
}

make_export_table() {
    local src="${CURVE_FILE:-$EXP_FILE}"
    [[ -n "$src" ]] || return 0
    cp "$src" "$OUTDIR/export/scattering_export.tsv"
    if [[ ! -f "$OUTDIR/export/scattering_export.json" ]]; then
        python3 - "$OUTDIR/export/scattering_export.json" "$LABEL" "$MODE" "$src" << 'PY'
import json, sys
out, label, mode, src = sys.argv[1:5]
with open(out, 'w', encoding='utf-8') as fh:
    json.dump({'label': label, 'mode': mode, 'source_curve': src}, fh, indent=2)
PY
    fi
}

make_plot() {
    command -v python3 >/dev/null 2>&1 || return 0
    python3 - "$OUTDIR" "$CURVE_FILE" "$EXP_FILE" << 'PY' >/dev/null 2>&1 || true
import sys, os
outdir, sim_path, exp_path = sys.argv[1:4]
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except Exception:
    raise SystemExit(0)

def read_curve(path):
    q, i = [], []
    if not path or not os.path.exists(path):
        return q, i
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not line.strip() or line.startswith('#'):
                continue
            parts = line.split()
            q.append(float(parts[0]))
            i.append(float(parts[1]))
    return q, i
qs, is_ = read_curve(sim_path)
qe, ie = read_curve(exp_path)
if not qs and not qe:
    raise SystemExit(0)
fig, axes = plt.subplots(1, 2 if qs or qe else 1, figsize=(10, 4))
if not isinstance(axes, (list, tuple)):
    axes = [axes]
ax = axes[0]
if qe:
    ax.plot(qe, ie, 'o', ms=3, label='experiment')
if qs:
    ax.plot(qs, is_, '-', lw=1.5, label='simulation')
ax.set_xlabel('q (1/nm)')
ax.set_ylabel('I(q)')
ax.set_title('Scattering curve')
ax.legend(frameon=False)
if len(axes) > 1:
    ax2 = axes[1]
    if qe:
        ax2.plot(qe, [q*q*i for q, i in zip(qe, ie)], 'o', ms=3, label='experiment')
    if qs:
        ax2.plot(qs, [q*q*i for q, i in zip(qs, is_)], '-', lw=1.5, label='simulation')
    ax2.set_xlabel('q (1/nm)')
    ax2.set_ylabel('q^2 I(q)')
    ax2.set_title('Kratky-like view')
    ax2.legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(outdir, 'figures', 'scattering_plot.png'), dpi=300)
PY
}

generate_report() {
    local mode_name="unknown"
    [[ -f "$OUTDIR/curves/mode.txt" ]] && mode_name="$(cat "$OUTDIR/curves/mode.txt")"
    local compare_txt=""
    local guinier_txt=""
    local kratky_txt=""
    [[ -f "$OUTDIR/compare/deviation_summary.txt" ]] && compare_txt="$(cat "$OUTDIR/compare/deviation_summary.txt")"
    [[ -f "$OUTDIR/interpret/guinier_summary.txt" ]] && guinier_txt="$(cat "$OUTDIR/interpret/guinier_summary.txt")"
    [[ -f "$OUTDIR/interpret/kratky_summary.txt" ]] && kratky_txt="$(cat "$OUTDIR/interpret/kratky_summary.txt")"
    cat > "$OUTDIR/SCATTERING_REPORT.md" << EOF
# Scattering Analysis Report

- Label: ${LABEL}
- Mode: ${MODE}
- Curve type: ${mode_name}
- Group: ${GROUP}
- q-range hint: ${QMIN:-auto} to ${QMAX:-auto} 1/nm
- Contrast factor: ${CONTRAST}
- Buffer density hint: ${BUFFER_DENSITY}

## Input Summary

- TPR: ${TPR:-N/A}
- Trajectory: ${TRJ:-N/A}
- Simulated curve: ${CURVE_FILE:-N/A}
- Experimental curve: ${EXP_FILE:-N/A}
- Existing SANS input: ${SANS_FILE:-N/A}

## Experiment Preparation Guidance

$(cat "$OUTDIR/compare/input_preparation_notes.md" 2>/dev/null || true)

## Simulation vs Experiment Comparison

\`\`\`
${compare_txt:-Comparison not requested or not available.}
\`\`\`

## Guinier Interpretation

\`\`\`
${guinier_txt:-Interpretation not requested or not available.}
\`\`\`

## Kratky Interpretation

\`\`\`
${kratky_txt:-Interpretation not requested or not available.}
\`\`\`

## Deliverables

\`\`\`
$(find "$OUTDIR" -maxdepth 2 -type f | sed "s#^$OUTDIR/##" | sort)
\`\`\`

## Visualization / Downstream Export

- Publication export: 
  - \`$OUTDIR/export/scattering_export.tsv\`
  - \`$OUTDIR/export/scattering_export.json\`
- If using publication-viz: supply cleaned \`curves/*.dat\` or comparison TSV.
- If using automd-viz: \`automd-viz --type data --input $OUTDIR/export/ --style nature\`

## Interpretation Notes

- Low-q bias usually reports shape/aggregation mismatch.
- Mid/high-q bias more often reports hydration, local packing, or force-field limitations.
- SANS disagreement should be interpreted together with contrast matching and isotope composition.
EOF
}

write_prep_notes
prepare_existing_curve
prepare_experiment

case "$MODE" in
    saxs)
        calc_saxs
        interpret_curve
        ;;
    sans)
        calc_sans
        interpret_curve
        ;;
    compare)
        compare_curves
        ;;
    interpret)
        interpret_curve
        ;;
    report)
        :
        ;;
    all)
        if [[ -n "$SANS_FILE" ]]; then
            calc_sans
        elif [[ -n "$TPR" && -n "$TRJ" ]]; then
            calc_saxs
        fi
        [[ -n "$EXP_FILE" && -n "$CURVE_FILE" ]] && compare_curves || true
        [[ -n "${CURVE_FILE:-$EXP_FILE}" ]] && interpret_curve || true
        ;;
    *) error "Unsupported mode: $MODE" ;;
esac

make_export_table
make_plot
generate_report

log "Scattering analysis complete: $OUTDIR/SCATTERING_REPORT.md"
echo ""
echo "Suggested next step: automd-viz --type data --input $OUTDIR/export/ --style nature"
exit 0
