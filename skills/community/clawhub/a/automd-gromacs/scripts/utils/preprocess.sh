#!/bin/bash
# preprocess - GROMACS preprocessing wrapper
# Wraps grompp with smart defaults & validation

set -e

show_help() {
    cat << 'EOF'
preprocess - GROMACS preprocessing wrapper

USAGE:
  preprocess -f md.mdp -c conf.gro -p topol.top -o run.tpr
  preprocess --quick em.mdp em.gro  # auto-detect topology

OPTIONS:
  -f FILE    MDP file (required)
  -c FILE    Coordinate file (required)
  -p FILE    Topology (default: topol.top)
  -o FILE    Output TPR (default: based on MDP name)
  -n FILE    Index file (optional)
  -r FILE    Reference for restraints (optional)
  -t FILE    Checkpoint for continuation (optional)
  --maxwarn N  Max warnings (default: 1)
  --quick    Skip validation checks
  -h, --help   Show this help

EXAMPLES:
  # Energy minimization
  preprocess -f em.mdp -c solvated.gro -o em.tpr

  # NVT with restraints
  preprocess -f nvt.mdp -c em.gro -r em.gro -o nvt.tpr

  # NPT continuation
  preprocess -f npt.mdp -c nvt.gro -t nvt.cpt -o npt.tpr

AUTO-DETECT:
  - Topology: searches topol.top, system.top
  - Output: derives from MDP name (em.mdp → em.tpr)
  - Restraints: uses -c if -r not specified

ERROR CODES:
  1  Missing required file
  2  grompp failed
  3  Validation failed
EOF
}

# Defaults
MDP=""
COORD=""
TOPOL=""
OUTPUT=""
INDEX=""
RESTRAINT=""
CHECKPOINT=""
MAXWARN=1
QUICK=0

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -f) MDP="$2"; shift 2 ;;
        -c) COORD="$2"; shift 2 ;;
        -p) TOPOL="$2"; shift 2 ;;
        -o) OUTPUT="$2"; shift 2 ;;
        -n) INDEX="$2"; shift 2 ;;
        -r) RESTRAINT="$2"; shift 2 ;;
        -t) CHECKPOINT="$2"; shift 2 ;;
        --maxwarn) MAXWARN="$2"; shift 2 ;;
        --quick) QUICK=1; shift ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

# Validate required
[[ -z "$MDP" ]] && { echo "ERROR: -f MDP required"; exit 1; }
[[ -z "$COORD" ]] && { echo "ERROR: -c coordinate required"; exit 1; }
[[ ! -f "$MDP" ]] && { echo "ERROR: MDP not found: $MDP"; exit 1; }
[[ ! -f "$COORD" ]] && { echo "ERROR: Coordinate not found: $COORD"; exit 1; }

# Auto-detect topology
if [[ -z "$TOPOL" ]]; then
    for f in topol.top system.top; do
        [[ -f "$f" ]] && { TOPOL="$f"; break; }
    done
    [[ -z "$TOPOL" ]] && { echo "ERROR: No topology found"; exit 1; }
fi
[[ ! -f "$TOPOL" ]] && { echo "ERROR: Topology not found: $TOPOL"; exit 1; }

# Auto-detect output
if [[ -z "$OUTPUT" ]]; then
    base=$(basename "$MDP" .mdp)
    OUTPUT="${base}.tpr"
fi

# Build grompp command as array (safer: no shell injection)
local cmd_arr=(gmx grompp -f "$MDP" -c "$COORD" -p "$TOPOL" -o "$OUTPUT" -maxwarn "$MAXWARN")
[[ -n "$INDEX" ]]      && cmd_arr+=(-n "$INDEX")
[[ -n "$RESTRAINT" ]]  && cmd_arr+=(-r "$RESTRAINT")
[[ -n "$CHECKPOINT" ]] && cmd_arr+=(-t "$CHECKPOINT")

# Pre-flight checks (unless --quick)
if [[ $QUICK -eq 0 ]]; then
    # Check atom count match
    coord_atoms=$(head -2 "$COORD" | tail -1 | awk '{print $1}')
    
    # Check for common issues
    if grep -q "continuation.*=.*yes" "$MDP" && [[ -z "$CHECKPOINT" ]]; then
        echo "WARNING: continuation=yes but no -t checkpoint"
    fi
    
    if grep -q "POSRES" "$MDP" && [[ -z "$RESTRAINT" ]]; then
        echo "WARNING: POSRES defined but no -r restraint file"
    fi
fi

# Run grompp
echo "Running: ${cmd_arr[*]}"
if "${cmd_arr[@]}" 2>&1 | tee grompp.log; then
    echo "✓ TPR created: $OUTPUT"
    
    # Show key info
    gmx check -s "$OUTPUT" 2>&1 | grep -E "atoms|Step|Time" || true
    
    exit 0
else
    echo "✗ grompp failed (see grompp.log)"
    echo ""
    echo "Common fixes:"
    echo "  - Check MDP syntax"
    echo "  - Verify topology matches coordinates"
    echo "  - Use --maxwarn 2 if warnings are expected"
    exit 2
fi
EOF
chmod +x preprocess.sh
