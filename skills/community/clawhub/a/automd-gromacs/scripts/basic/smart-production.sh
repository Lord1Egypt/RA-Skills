#!/bin/bash
# smart-production.sh - 智能生产MD模拟
# Features: auto-checkpoint-resume, real-time monitoring, self-tuning
set -e

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# === Auto-detect environment ===
auto_detect() {
    # CPU cores
    CORES=$(nproc 2>/dev/null || echo 4)
    # Memory (GB)
    MEM=$(free -g 2>/dev/null | awk '/^Mem:/{print $2}' || echo 8)
    # GROMACS
    GMX_VERSION=$(gmx --version 2>&1 | grep 'GROMACS version' | awk '{print $3}' || echo "unknown")
    
    echo "=== System ==="
    echo "  GROMACS: $GMX_VERSION"
    echo "  CPU cores: $CORES"
    echo "  Memory: ${MEM} GB"
}

# === Real-time monitor ===
start_monitor() {
    local deffnm=$1
    local logfile="${deffnm}.log"
    local edrfile="${deffnm}.edr"
    local monitor_pid_file="/tmp/gmx_monitor_${deffnm}.pid"
    
    # Background monitor
    (
        echo $$ > "$monitor_pid_file"
        sleep 5  # Wait for mdrun to start
        
        while kill -0 $$ 2>/dev/null; do
            if [ -f "$logfile" ]; then
                # Progress
                local step=$(grep -a "step=" "$logfile" 2>/dev/null | tail -1 | grep -oP 'step=\s*\K[0-9]+' || echo "?")
                # Performance
                local perf=$(grep -a "Performance:" "$logfile" 2>/dev/null | tail -1 | awk '{print $2}' || echo "?")
                echo "[MONITOR] step=${step} perf=${perf} ns/day"
            fi
            sleep 30
        done
    ) &
    MONITOR_PID=$!
    echo "  Monitor PID: $MONITOR_PID"
}

stop_monitor() {
    [ -n "$MONITOR_PID" ] && kill $MONITOR_PID 2>/dev/null || true
}

# === Parse args ===
INPUT=""
TOPOLOGY=""
OUTPUT="md"
TIME=1000
CORES=""
RESUME=1  # Auto-resume by default

while [[ $# -gt 0 ]]; do
  case $1 in
    --input|-i) INPUT="$2"; shift 2 ;;
    --topology|-t) TOPOLOGY="$2"; shift 2 ;;
    --output|-o) OUTPUT="$2"; shift 2 ;;
    --time|-T) TIME="$2"; shift 2 ;;
    --cores|-c) CORES="$2"; shift 2 ;;
    --no-resume) RESUME=0; shift ;;
    *) log "Unknown: $1"; shift ;;
  esac
done

# Auto-detect cores
[ -z "$CORES" ] && CORES=$(nproc)
log "Using ${CORES} cores"

# Validate
for f in "$INPUT" "$TOPOLOGY"; do
    [ -f "$f" ] || { log "ERROR: Missing $f"; exit 1; }
done

# === Checkpoint resume ===
CPT_FILE="${OUTPUT}.cpt"
RESUME_FLAG=""
if [ "$RESUME" = "1" ] && [ -f "${OUTPUT}.cpt" ]; then
    log "📌 Found checkpoint: ${OUTPUT}.cpt"
    # Check if simulation already finished
    if [ -f "${OUTPUT}.log" ]; then
        FINISHED=$(grep -c "Finished mdrun" "${OUTPUT}.log" 2>/dev/null || echo 0)
        if [ "$FINISHED" -gt 0 ]; then
            log "✅ Simulation already completed! Skipping."
            exit 0
        fi
    fi
    RESUME_FLAG="-cpi ${OUTPUT}.cpt -noappend"
    log "Resuming from checkpoint..."
fi

# === Generate MDP ===
NSTEPS=$((TIME * 500))
cat > ${OUTPUT}.mdp << EOF
integrator = md
dt = 0.002
nsteps = $NSTEPS
nstxout = 0
nstvout = 0
nstfout = 0
nstlog = 5000
nstenergy = 5000
nstxout-compressed = 5000
constraints = h-bonds
constraint-algorithm = lincs
lincs-iter = 1
lincs-order = 4
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau-t = 0.1 0.1
ref-t = 300 300
pcoupl = Parrinello-Rahman
pcoupltype = isotropic
tau-p = 2.0
ref-p = 1.0
compressibility = 4.5e-5
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.12
vdwtype = Cut-off
rvdw = 1.2
DispCorr = EnerPres
pbc = xyz
EOF

log "Generated ${OUTPUT}.mdp ($TIME ps, $NSTEPS steps)"

# === Grompp ===
log "Running grompp..."
if [ -n "$RESUME_FLAG" ]; then
    gmx grompp -f ${OUTPUT}.mdp -c "$INPUT" -p "$TOPOLOGY" \
        -o ${OUTPUT}_new.tpr -maxwarn 1 2>&1 | tail -1
    # For checkpoint resume, use original TPR + cpt
    if [ -f "${OUTPUT}.tpr" ]; then
        log "Using existing TPR for resume"
    fi
else
    gmx grompp -f ${OUTPUT}.mdp -c "$INPUT" -p "$TOPOLOGY" \
        -o ${OUTPUT}.tpr -maxwarn 1 2>&1 | tail -1
fi

# === Run ===
log "Starting mdrun (${TIME} ps on ${CORES} cores)..."
start_monitor "$OUTPUT"

START_TIME=$(date +%s)

gmx mdrun -v -deffnm ${OUTPUT} -nt $CORES $RESUME_FLAG 2>&1 | tail -5
MD_EXIT=$?

stop_monitor

ELAPSED=$(( $(date +%s) - START_TIME ))
log "mdrun finished in ${ELAPSED}s (exit=$MD_EXIT)"

# === Quick analysis ===
if [ -f "${OUTPUT}.edr" ]; then
    printf "1\n0\n" | gmx energy -f ${OUTPUT}.edr -o /tmp/_temp.xvg 2>/dev/null
    TEMP_AVG=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.1f", sum/n}' /tmp/_temp.xvg 2>/dev/null || echo "?")
    printf "2\n0\n" | gmx energy -f ${OUTPUT}.edr -o /tmp/_press.xvg 2>/dev/null
    PRESS_AVG=$(awk '/^[^#@]/ {sum+=$2; n++} END {printf "%.0f", sum/n}' /tmp/_press.xvg 2>/dev/null || echo "?")
    
    echo ""
    echo "=== Production Summary ==="
    echo "  Time:       ${TIME} ps"
    echo "  Temperature: ${TEMP_AVG} K (target: 300 K)"
    echo "  Pressure:    ${PRESS_AVG} bar (target: 1 bar)"
    echo "  Wall time:   ${ELAPSED}s"
    
    if [ -f "${OUTPUT}.log" ]; then
        PERF=$(grep -a "Performance:" ${OUTPUT}.log 2>/dev/null | tail -1 | awk '{print $2}')
        echo "  Performance: ${PERF:-?} ns/day"
    fi
    echo ""
    echo "  Files:"
    echo "    ${OUTPUT}.xtc  - Trajectory"
    echo "    ${OUTPUT}.edr  - Energy"
    echo "    ${OUTPUT}.cpt  - Checkpoint"
    echo "    ${OUTPUT}.log  - Log"
fi

log "✅ Done"
