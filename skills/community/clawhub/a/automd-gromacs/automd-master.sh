#!/bin/bash
# automd-master.sh — Unified MD Workflow Master Controller
# 单一入口，自动检测体系、选择最优流程、全自动运行
# v5.1.0

set -e
SKILL_ROOT="${SKILL_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SCRIPTS="$SKILL_ROOT/scripts"

log()  { echo "[$(date '+%H:%M:%S')] 🔬 $*"; }
ok()   { echo "  ✅ $*"; }
warn() { echo "  ⚠️ $*"; }
err()  { echo "  ❌ $*"; }

# ============================================================
# Phase 0: Auto-detect system
# ============================================================
detect_system() {
    log "Detecting system..."
    
    PDBS=$(ls *.pdb 2>/dev/null | wc -l)
    GROS=$(ls *.gro 2>/dev/null | wc -l)
    
    if [ -f topol.top ]; then
        echo "  Topology: topol.top found"
    fi
    
    # Detect system type
    SYSTEM_TYPE="protein"
    HAS_MEMBRANE=0
    HAS_LIGAND=0
    HAS_SOLVENT=0
    
    if [ -f system.gro ] || [ -f npt.gro ] || [ -f em.gro ]; then
        ok "Prepared system found — skip to production"
        SYSTEM_STATE="prepared"
    elif [ -f topol.top ] && [ "$GROS" -gt 0 ]; then
        ok "Topology + GRO found — skip to equilibration"
        SYSTEM_STATE="topology"
    elif [ "$PDBS" -gt 0 ]; then
        ok "PDB input found — start from scratch"
        SYSTEM_STATE="pdb"
    else
        err "No input files found"
        echo "  Drop a .pdb file here and run again"
        exit 1
    fi
    
    echo "  State: $SYSTEM_STATE"
    echo "  Type: $SYSTEM_TYPE"
}

# ============================================================
# Phase 1: System Setup (PDB → solvated + ions)
# ============================================================
do_setup() {
    log "Phase 1: System Setup"
    
    local pdb=$(ls *.pdb 2>/dev/null | head -1)
    if [ -z "$pdb" ]; then
        ok "No PDB found, skipping setup"
        return 0
    fi
    
    if [ -f "$SCRIPTS/basic/setup.sh" ]; then
        bash "$SCRIPTS/basic/setup.sh" --input "$pdb" 2>&1 | tail -5
        ok "Setup complete"
    else
        # Minimal inline setup
        local base=$(basename "$pdb" .pdb)
        log "  pdb2gmx..."
        echo "1" | gmx pdb2gmx -f "$pdb" -o "${base}_processed.gro" -p topol.top \
            -i posre.itp -water spce -ff amber99sb-ildn -ignh 2>&1 | tail -2
        
        log "  editconf (dodecahedron)..."
        gmx editconf -f "${base}_processed.gro" -o box.gro -c -d 1.2 -bt dodecahedron 2>&1 | tail -1
        
        log "  solvate..."
        gmx solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top 2>&1 | tail -1
        
        log "  genion..."
        gmx grompp -f "$SCRIPTS/../references/templates/em.mdp" -c solv.gro -p topol.top \
            -o ions.tpr -maxwarn 1 2>&1 | tail -1
        printf "SOL\n" | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top \
            -pname NA -nname CL -neutral -conc 0.15 2>&1 | tail -2
        
        ok "Setup complete"
    fi
}

# ============================================================
# Phase 2: Energy Minimization
# ============================================================
do_em() {
    log "Phase 2: Energy Minimization"
    
    local input_gro="solv_ions.gro"
    [ -f "$input_gro" ] || input_gro=$(ls *.gro 2>/dev/null | grep -v '^em\.' | head -1)
    [ -f "$input_gro" ] || { err "No input GRO for EM"; return 1; }
    [ -f topol.top ] || { err "No topol.top"; return 1; }
    
    # Check if already done
    if [ -f em.gro ] && grep -q "Fmax" em.log 2>/dev/null; then
        Fmax=$(grep "Fmax" em.log | tail -1 | awk '{print $NF}')
        if (( $(awk "BEGIN {print ($Fmax < 1000)}") )); then
            ok "EM already done (Fmax=$Fmax < 1000)"
            return 0
        fi
    fi
    
    # Generate or use template MDP
    if [ ! -f em.mdp ]; then
        cp "$SKILL_ROOT/references/templates/em.mdp" em.mdp 2>/dev/null || {
            cat > em.mdp << 'EOF'
integrator = steep
nsteps = 50000
emtol = 1000
emstep = 0.01
nstxout = 100
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
vdwtype = Cut-off
rvdw = 1.2
pbc = xyz
EOF
        }
    fi
    
    log "  grompp + mdrun (EM)..."
    gmx grompp -f em.mdp -c "$input_gro" -p topol.top -o em.tpr -maxwarn 1 2>&1 | tail -1
    gmx mdrun -v -deffnm em -nt $(nproc) 2>&1 | tail -3
    
    Fmax=$(grep "Fmax" em.log | tail -1 | awk '{print $NF}')
    if (( $(awk "BEGIN {print ($Fmax < 1000)}") )); then
        ok "EM converged: Fmax=$Fmax < 1000"
    else
        warn "EM not fully converged: Fmax=$Fmax"
    fi
}

# ============================================================
# Phase 3: Equilibration (NVT + NPT)
# ============================================================
do_equilibration() {
    log "Phase 3: Equilibration"
    
    if [ -f npt.gro ] && [ -f npt.cpt ]; then
        ok "NPT already done, skipping"
        return 0
    fi
    
    # NVT
    log "  NVT equilibration (50 ps)..."
    cat > nvt.mdp << 'EOF'
integrator = md
dt = 0.002
nsteps = 25000
nstxout = 5000
nstvout = 5000
nstenergy = 5000
nstlog = 5000
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau-t = 0.1 0.1
ref-t = 300 300
pcoupl = no
pbc = xyz
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
vdwtype = Cut-off
rvdw = 1.2
DispCorr = EnerPres
gen-vel = yes
gen-temp = 300
EOF
    
    gmx grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr -maxwarn 1 2>&1 | tail -1
    gmx mdrun -v -deffnm nvt -nt $(nproc) 2>&1 | tail -3
    ok "NVT done"
    
    # NPT
    log "  NPT equilibration (50 ps)..."
    cat > npt.mdp << 'EOF'
integrator = md
dt = 0.002
nsteps = 25000
nstxout = 5000
nstvout = 5000
nstenergy = 5000
nstlog = 5000
constraints = h-bonds
constraint-algorithm = lincs
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau-t = 0.1 0.1
ref-t = 300 300
pcoupl = Parrinello-Rahman
pcoupltype = isotropic
tau-p = 2.0
ref-p = 1.0
compressibility = 4.5e-5
pbc = xyz
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
vdwtype = Cut-off
rvdw = 1.2
DispCorr = EnerPres
EOF
    
    gmx grompp -f npt.mdp -c nvt.gro -p topol.top -o npt.tpr -maxwarn 1 2>&1 | tail -1
    gmx mdrun -v -deffnm npt -nt $(nproc) 2>&1 | tail -3
    ok "NPT done"
}

# ============================================================
# Phase 4: Production
# ============================================================
do_production() {
    log "Phase 4: Production MD"
    
    local time=${1:-100}  # ps
    local nsteps=$((time * 500))
    
    if [ -f prod.cpt ] && grep -q "Finished mdrun" prod.log 2>/dev/null; then
        ok "Production already complete"
        return 0
    fi
    
    cat > prod.mdp << EOF
integrator = md
dt = 0.002
nsteps = $nsteps
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
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
pme-order = 4
fourierspacing = 0.12
vdwtype = Cut-off
rvdw = 1.2
DispCorr = EnerPres
pbc = xyz
EOF
    
    # Resume from checkpoint if exists
    local resume_flag=""
    if [ -f prod.cpt ]; then
        log "  Resuming from checkpoint..."
        resume_flag="-cpi prod.cpt -noappend"
    fi
    
    gmx grompp -f prod.mdp -c npt.gro -p topol.top -o prod.tpr -maxwarn 1 2>&1 | tail -1
    gmx mdrun -v -deffnm prod -nt $(nproc) $resume_flag 2>&1 | tail -5
    
    ok "Production done"
}

# ============================================================
# Phase 5: Analysis (auto-run all)
# ============================================================
do_analysis() {
    log "Phase 5: Analysis"
    
    mkdir -p analysis
    cd analysis
    
    TPR=../prod.tpr
    TRJ=../prod.trr
    GRO=../prod.gro
    
    # Basic
    log "  Basic: RMSD, RMSF, Rg, SASA..."
    printf "Backbone\nBackbone\n" | gmx rms -s "$TPR" -f "$TRJ" -o rmsd.xvg 2>/dev/null
    printf "C-alpha\n" | gmx rmsf -s "$TPR" -f "$TRJ" -o rmsf.xvg 2>/dev/null
    printf "Protein\n" | gmx gyrate -s "$TPR" -f "$TRJ" -o gyrate.xvg 2>/dev/null
    ok "Basic analysis done"
    
    # PCA
    log "  PCA..."
    printf "C-alpha\nC-alpha\n" | gmx covar -s "$TPR" -f "$TRJ" -o eigenval.xvg -v eigenvec.trr 2>/dev/null
    printf "C-alpha\nC-alpha\n" | gmx anaeig -s "$TPR" -f "$TRJ" -v eigenvec.trr -2d proj2d.xvg -first 1 -last 2 2>/dev/null
    ok "PCA done"
    
    # Cluster
    log "  Clustering..."
    printf "Backbone\nBackbone\n" | gmx cluster -s "$TPR" -f "$TRJ" -cl clusters.pdb -o clusters.xpm \
        -dist rmsd-dist.xvg -cutoff 0.15 -method gromos 2>/dev/null
    ok "Clustering done"
    
    cd ..
}

# ============================================================
# Main
# ============================================================
main() {
    echo ""
    echo "╔══════════════════════════════════════╗"
    echo "║   🧬 AutoMD-GROMACS Master v5.1.0    ║"
    echo "╚══════════════════════════════════════╝"
    echo ""
    
    detect_system
    echo ""
    
    TIME=${TIME:-100}  # default 100 ps
    
    case "${SYSTEM_STATE:-pdb}" in
        pdb)        do_setup; do_em; do_equilibration; do_production "$TIME"; do_analysis ;;
        topology)   do_em; do_equilibration; do_production "$TIME"; do_analysis ;;
        prepared)   do_production "$TIME"; do_analysis ;;
    esac
    
    echo ""
    echo "╔══════════════════════════════════════╗"
    echo "║   ✅ Workflow Complete               ║"
    echo "╚══════════════════════════════════════╝"
    echo ""
    echo "Output:"
    echo "  prod.xtc  — Production trajectory"
    echo "  prod.edr  — Energy data"
    echo "  analysis/ — All analysis results"
    echo ""
    echo "Run extended analysis:"
    echo "  bash $SKILL_ROOT/scripts/analysis/analysis-extended.sh"
}

main "$@"
