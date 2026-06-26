#!/bin/bash
# utils - GROMACS utility toolkit
# Common operations: trjconv, editconf, make_ndx

set -e

show_help() {
    cat << 'EOF'
utils - GROMACS utility toolkit

COMMANDS:
  center      Center system & remove PBC
  fit         Fit trajectory to reference
  extract     Extract frames from trajectory
  makebox     Define simulation box
  makeindex   Create custom index groups
  convert     Convert file formats

USAGE:
  utils center -s md.tpr -f md.xtc -o centered.xtc
  utils fit -s md.tpr -f md.xtc -o fitted.xtc
  utils extract -f md.xtc -b 5000 -e 10000 -o window.xtc
  utils makebox -f protein.gro -d 1.0 -bt dodecahedron
  utils makeindex -f system.gro -o index.ndx
  utils convert -f traj.trr -o traj.xtc

OPTIONS (vary by command):
  -s FILE    Structure/TPR file
  -f FILE    Input trajectory/coordinate
  -o FILE    Output file
  -b TIME    Begin time (ps)
  -e TIME    End time (ps)
  -dt TIME   Frame interval (ps)
  -d DIST    Box distance (nm)
  -bt TYPE   Box type (cubic/dodecahedron/octahedron)
  -skip N    Skip every N frames
  --group    Selection group (Protein/System/etc)

EXAMPLES:
  # Remove PBC & center protein
  utils center -s md.tpr -f md.xtc -o clean.xtc

  # Fit to reference structure
  utils fit -s md.tpr -f md.xtc -o fitted.xtc

  # Extract 5-10 ns
  utils extract -f md.xtc -b 5000 -e 10000 -o segment.xtc

  # Create box with 1.2 nm margin
  utils makebox -f protein.gro -d 1.2 -bt cubic

  # Create custom index
  utils makeindex -f system.gro -o index.ndx
EOF
}

# Parse command
CMD="${1:-}"
shift || true

case "$CMD" in
    center)
        # Center & remove PBC
        TPR=""
        TRJ=""
        OUT="centered.xtc"
        GROUP="Protein"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                --group) GROUP="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        
        echo "Centering on $GROUP & removing PBC..."
        echo "$GROUP System" | gmx trjconv -s "$TPR" -f "$TRJ" -o "$OUT" -pbc mol -center -ur compact
        echo "✓ Output: $OUT"
        ;;
        
    fit)
        # Fit trajectory
        TPR=""
        TRJ=""
        OUT="fitted.xtc"
        GROUP="Backbone"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                --group) GROUP="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        
        echo "Fitting to $GROUP..."
        echo "$GROUP $GROUP" | gmx trjconv -s "$TPR" -f "$TRJ" -o "$OUT" -fit rot+trans
        echo "✓ Output: $OUT"
        ;;
        
    extract)
        # Extract time window
        TRJ=""
        OUT="extracted.xtc"
        BEGIN=""
        END=""
        DT=""
        SKIP=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -f) TRJ="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                -dt) DT="$2"; shift 2 ;;
                -skip) SKIP="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TRJ" ]] && { echo "ERROR: -f required"; exit 1; }
        
        # Build command as array (safer: no shell injection)
        local cmd_arr=(gmx trjconv -f "$TRJ" -o "$OUT")
        [[ -n "$BEGIN" ]] && cmd_arr+=(-b "$BEGIN")
        [[ -n "$END" ]]   && cmd_arr+=(-e "$END")
        [[ -n "$DT" ]]    && cmd_arr+=(-dt "$DT")
        [[ -n "$SKIP" ]]  && cmd_arr+=(-skip "$SKIP")
        
        echo "Extracting frames..."
        echo "System" | "${cmd_arr[@]}"
        echo "✓ Output: $OUT"
        ;;
        
    makebox)
        # Define box
        GRO=""
        OUT="boxed.gro"
        DIST="1.0"
        BOXTYPE="dodecahedron"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -f) GRO="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                -d) DIST="$2"; shift 2 ;;
                -bt) BOXTYPE="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$GRO" ]] && { echo "ERROR: -f required"; exit 1; }
        
        echo "Creating $BOXTYPE box with $DIST nm margin..."
        gmx editconf -f "$GRO" -o "$OUT" -c -d "$DIST" -bt "$BOXTYPE"
        echo "✓ Output: $OUT"
        
        # Show box info
        tail -1 "$OUT"
        ;;
        
    makeindex)
        # Create index
        GRO=""
        OUT="index.ndx"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -f) GRO="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$GRO" ]] && { echo "ERROR: -f required"; exit 1; }
        
        echo "Creating index file (interactive)..."
        echo "Available commands:"
        echo "  a CA        - select all CA atoms"
        echo "  r 1-50      - select residues 1-50"
        echo "  1 | 13      - combine groups"
        echo "  name 20 X   - name group 20 as X"
        echo "  q           - quit"
        echo ""
        gmx make_ndx -f "$GRO" -o "$OUT"
        echo "✓ Output: $OUT"
        ;;
        
    convert)
        # Format conversion
        IN=""
        OUT=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -f) IN="$2"; shift 2 ;;
                -o) OUT="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$IN" || -z "$OUT" ]] && { echo "ERROR: -f and -o required"; exit 1; }
        
        echo "Converting $IN → $OUT..."
        echo "System" | gmx trjconv -f "$IN" -o "$OUT"
        echo "✓ Output: $OUT"
        ;;
        
    -h|--help|"")
        show_help
        exit 0
        ;;
        
    *)
        echo "Unknown command: $CMD"
        echo "Run 'utils --help' for usage"
        exit 1
        ;;
esac
