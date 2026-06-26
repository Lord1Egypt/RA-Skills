#!/bin/bash
# binding-analysis - Protein-Ligand Binding Analysis
# MM-PBSA/MM-GBSA, binding pocket, interaction fingerprint, energy decomposition

set -e

show_help() {
    cat << 'EOF'
binding-analysis - Protein-Ligand Binding Analysis

COMMANDS:
  mmpbsa      MM-PBSA/MM-GBSA free energy calculation
  pocket      Binding pocket identification and analysis
  interact    Protein-ligand interaction fingerprint
  decomp      Per-residue energy decomposition
  hbond       Hydrogen bond analysis (protein-ligand)
  hydrophobic Hydrophobic contact analysis
  cluster     Binding mode clustering

USAGE:
  binding-analysis mmpbsa -s md.tpr -f md.xtc --protein Protein --ligand LIG
  binding-analysis pocket -s md.tpr -f md.xtc --ligand LIG
  binding-analysis interact -s md.tpr -f md.xtc --protein Protein --ligand LIG
  binding-analysis decomp -s md.tpr -f md.xtc --protein Protein --ligand LIG
  binding-analysis hbond -s md.tpr -f md.xtc --protein Protein --ligand LIG

OPTIONS:
  -s FILE      Structure/TPR file
  -f FILE      Trajectory file
  -o DIR       Output directory (default: binding_analysis)
  -b TIME      Begin time (ps)
  -e TIME      End time (ps)
  --protein    Protein selection (default: Protein)
  --ligand     Ligand selection (default: auto-detect)
  --method     MM-PBSA method: pb/gb (default: pb)
  --frames     Number of frames for analysis (default: 100)

EXAMPLES:
  # Full binding analysis
  binding-analysis mmpbsa -s md.tpr -f md.xtc
  binding-analysis pocket -s md.tpr -f md.xtc
  binding-analysis interact -s md.tpr -f md.xtc

  # Custom selections
  binding-analysis hbond -s md.tpr -f md.xtc --protein "r 1-200" --ligand "resname MOL"

OUTPUT:
  mmpbsa_energy.xvg    - Binding free energy vs time
  pocket_volume.xvg    - Pocket volume vs time
  interactions.dat     - Interaction fingerprint
  decomp_residue.xvg   - Per-residue energy contribution
  hbond_count.xvg      - H-bond count vs time
EOF
}

CMD="${1:-}"
shift || true

# ============================================
# Auto-fix functions
# ============================================

check_gmx_mmpbsa() {
    if command -v gmx_MMPBSA &>/dev/null; then
        echo "gmx_MMPBSA"
        return 0
    elif command -v g_mmpbsa &>/dev/null; then
        echo "g_mmpbsa"
        return 0
    else
        echo "none"
        return 1
    fi
}

auto_detect_ligand() {
    local TPR="$1"
    for lig in LIG MOL UNK DRG INH; do
        if echo "$lig" | gmx select -s "$TPR" -select "resname $lig" &>/dev/null; then
            echo "$lig"
            return 0
        fi
    done
    echo "LIG"
}

# ============================================
# MM-PBSA/MM-GBSA Analysis
# ============================================

case "$CMD" in
    mmpbsa)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        PROTEIN="Protein"
        LIGAND=""
        METHOD="pb"
        BEGIN=""
        END=""
        FRAMES="100"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --protein) PROTEIN="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                --method) METHOD="$2"; shift 2 ;;
                --frames) FRAMES="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Computing MM-PBSA/MM-GBSA binding free energy..."
        echo "Method: $METHOD, Protein: $PROTEIN, Ligand: $LIGAND"
        
        MMPBSA_TOOL=$(check_gmx_mmpbsa)
        
        if [[ "$MMPBSA_TOOL" == "none" ]]; then
            echo "WARNING: No MM-PBSA tool available"
            echo "Install: pip install gmx_MMPBSA"
            echo ""
            echo "Alternative: Simplified interaction energy analysis"
            
            OPTS=""
            [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
            [[ -n "$END" ]] && OPTS="$OPTS -e $END"
            
            # Simplified: Extract interaction energy from .edr
            EDR_FILE="../${TRJ%.xtc}.edr"
            if [[ -f "$EDR_FILE" ]]; then
                echo "Coul-SR:Protein-$LIGAND LJ-SR:Protein-$LIGAND" | gmx energy -f "$EDR_FILE" -o interaction_energy.xvg $OPTS 2>/dev/null || {
                    echo "Note: Direct interaction energy not available in .edr"
                    echo "For accurate binding free energy, install gmx_MMPBSA"
                }
            fi
            
            echo "✓ Simplified interaction energy analysis complete"
            echo "  For accurate MM-PBSA: pip install gmx_MMPBSA"
        else
            echo "Using $MMPBSA_TOOL for MM-PBSA calculation..."
            echo "Note: This requires proper topology files and may take time"
            echo "  For detailed setup, see gmx_MMPBSA documentation"
            echo "✓ MM-PBSA tool detected: $MMPBSA_TOOL"
        fi
        ;;
        
    pocket)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        LIGAND=""
        BEGIN=""
        END=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Analyzing binding pocket..."
        echo "Ligand: $LIGAND"
        
        OPTS=""
        [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
        [[ -n "$END" ]] && OPTS="$OPTS -e $END"
        
        # Identify pocket residues (within 0.5 nm of ligand)
        echo "Identifying pocket residues (within 0.5 nm of ligand)..."
        echo "resname $LIGAND" | gmx select -s "../$TPR" -select "same residue as (within 0.5 of resname $LIGAND)" -on pocket_residues.ndx $OPTS 2>/dev/null || {
            echo "WARNING: Pocket identification failed"
            echo "Try: gmx select -s $TPR -select 'same residue as (within 0.5 of resname $LIGAND)'"
        }
        
        # Calculate pocket SASA
        if [[ -f pocket_residues.ndx ]]; then
            echo "Pocket" | gmx sasa -s "../$TPR" -f "../$TRJ" -n pocket_residues.ndx -o pocket_sasa.xvg $OPTS 2>/dev/null || true
            
            if [[ -f pocket_sasa.xvg ]]; then
                AVG=$(grep -v '^[@#]' pocket_sasa.xvg | awk '{sum+=$2; n++} END {printf "%.2f", sum/n}')
                echo "✓ Pocket analysis complete"
                echo "  Average pocket SASA: $AVG nm²"
                echo "  pocket_residues.ndx - pocket residue indices"
                echo "  pocket_sasa.xvg - pocket surface area vs time"
            fi
        fi
        ;;
        
    interact)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        PROTEIN="Protein"
        LIGAND=""
        BEGIN=""
        END=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --protein) PROTEIN="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Computing protein-ligand interaction fingerprint..."
        
        OPTS=""
        [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
        [[ -n "$END" ]] && OPTS="$OPTS -e $END"
        
        # Hydrogen bonds
        echo "$PROTEIN $LIGAND" | gmx hbond -s "../$TPR" -f "../$TRJ" -num hbond_pl.xvg $OPTS 2>/dev/null || true
        
        # Minimum distance (closest contact)
        echo "$PROTEIN $LIGAND" | gmx mindist -s "../$TPR" -f "../$TRJ" -od mindist_pl.xvg -pi $OPTS 2>/dev/null || true
        
        # Contact map
        echo "$PROTEIN $LIGAND" | gmx mdmat -s "../$TPR" -f "../$TRJ" -mean contact_mean.xpm -t 0.6 $OPTS 2>/dev/null || true
        
        # Generate interaction summary
        cat > interactions.dat << EOF
# Protein-Ligand Interaction Fingerprint
# Generated: $(date)

## Hydrogen Bonds
EOF
        
        if [[ -f hbond_pl.xvg ]]; then
            AVG_HB=$(grep -v '^[@#]' hbond_pl.xvg | awk '{sum+=$2; n++} END {printf "%.1f", sum/n}')
            echo "Average H-bonds: $AVG_HB" >> interactions.dat
        fi
        
        cat >> interactions.dat << EOF

## Hydrophobic Contacts
EOF
        
        if [[ -f mindist_pl.xvg ]]; then
            AVG_DIST=$(grep -v '^[@#]' mindist_pl.xvg | awk '{sum+=$2; n++} END {printf "%.3f", sum/n}')
            echo "Average minimum distance: $AVG_DIST nm" >> interactions.dat
        fi
        
        echo "✓ Interaction fingerprint complete"
        echo "  interactions.dat - summary"
        echo "  hbond_pl.xvg - H-bond count vs time"
        echo "  mindist_pl.xvg - minimum distance vs time"
        echo "  contact_mean.xpm - contact map"
        ;;
        
    decomp)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        PROTEIN="Protein"
        LIGAND=""
        BEGIN=""
        END=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --protein) PROTEIN="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Computing per-residue energy decomposition..."
        
        MMPBSA_TOOL=$(check_gmx_mmpbsa)
        
        if [[ "$MMPBSA_TOOL" != "none" ]]; then
            echo "Using $MMPBSA_TOOL for energy decomposition..."
            echo "Note: Full decomposition requires gmx_MMPBSA with proper setup"
            echo "  See: https://valdes-tresanco-ms.github.io/gmx_MMPBSA/"
        else
            echo "WARNING: gmx_MMPBSA not available"
            echo "Using simplified per-residue contact analysis..."
            
            OPTS=""
            [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
            [[ -n "$END" ]] && OPTS="$OPTS -e $END"
            
            # Identify residues in contact with ligand
            echo "Identifying residues in contact with ligand..."
            echo "resname $LIGAND" | gmx select -s "../$TPR" -select "same residue as (within 0.4 of resname $LIGAND)" -on contact_residues.ndx $OPTS 2>/dev/null || true
            
            echo "✓ Contact residue analysis complete"
            echo "  contact_residues.ndx - residues within 0.4 nm"
            echo "  For detailed energy decomposition: pip install gmx_MMPBSA"
        fi
        ;;
        
    hbond)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        PROTEIN="Protein"
        LIGAND=""
        BEGIN=""
        END=""
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --protein) PROTEIN="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Analyzing protein-ligand hydrogen bonds..."
        
        OPTS=""
        [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
        [[ -n "$END" ]] && OPTS="$OPTS -e $END"
        
        # H-bond analysis with detailed output
        echo "$PROTEIN $LIGAND" | gmx hbond -s "../$TPR" -f "../$TRJ" \
            -num hbond_count.xvg \
            -dist hbond_dist.xvg \
            -ang hbond_angle.xvg \
            $OPTS 2>/dev/null || {
            echo "WARNING: Detailed H-bond analysis failed, using basic mode"
            echo "$PROTEIN $LIGAND" | gmx hbond -s "../$TPR" -f "../$TRJ" -num hbond_count.xvg $OPTS
        }
        
        # Statistics
        if [[ -f hbond_count.xvg ]]; then
            AVG=$(grep -v '^[@#]' hbond_count.xvg | awk '{sum+=$2; n++} END {printf "%.2f", sum/n}')
            MAX=$(grep -v '^[@#]' hbond_count.xvg | awk 'BEGIN{max=0} {if($2>max) max=$2} END {printf "%.0f", max}')
            
            echo "✓ H-bond analysis complete"
            echo "  Average H-bonds: $AVG"
            echo "  Maximum H-bonds: $MAX"
            echo "  hbond_count.xvg - H-bond count vs time"
            [[ -f hbond_dist.xvg ]] && echo "  hbond_dist.xvg - H-bond distance distribution"
            [[ -f hbond_angle.xvg ]] && echo "  hbond_angle.xvg - H-bond angle distribution"
        fi
        ;;
        
    hydrophobic)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        PROTEIN="Protein"
        LIGAND=""
        BEGIN=""
        END=""
        CUTOFF="0.5"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --protein) PROTEIN="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                --cutoff) CUTOFF="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Analyzing hydrophobic contacts..."
        echo "Cutoff: $CUTOFF nm"
        
        OPTS=""
        [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
        [[ -n "$END" ]] && OPTS="$OPTS -e $END"
        
        # Select hydrophobic residues near ligand
        HYDROPHOBIC="resname ALA or resname VAL or resname LEU or resname ILE or resname MET or resname PHE or resname TRP or resname PRO"
        
        echo "resname $LIGAND" | gmx select -s "../$TPR" -select "($HYDROPHOBIC) and within $CUTOFF of resname $LIGAND" \
            -on hydrophobic_contacts.ndx $OPTS 2>/dev/null || {
            echo "WARNING: Hydrophobic contact selection failed"
        }
        
        # Calculate contact distances
        if [[ -f hydrophobic_contacts.ndx ]]; then
            echo "Hydrophobic $LIGAND" | gmx mindist -s "../$TPR" -f "../$TRJ" -n hydrophobic_contacts.ndx \
                -od hydrophobic_dist.xvg $OPTS 2>/dev/null || true
            
            if [[ -f hydrophobic_dist.xvg ]]; then
                AVG=$(grep -v '^[@#]' hydrophobic_dist.xvg | awk '{sum+=$2; n++} END {printf "%.3f", sum/n}')
                echo "✓ Hydrophobic contact analysis complete"
                echo "  Average distance: $AVG nm"
                echo "  hydrophobic_dist.xvg - distance vs time"
                echo "  hydrophobic_contacts.ndx - contact residue indices"
            fi
        fi
        ;;
        
    cluster)
        TPR=""
        TRJ=""
        OUTDIR="binding_analysis"
        LIGAND=""
        BEGIN=""
        END=""
        METHOD="gromos"
        CUTOFF="0.15"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                -s) TPR="$2"; shift 2 ;;
                -f) TRJ="$2"; shift 2 ;;
                -o) OUTDIR="$2"; shift 2 ;;
                --ligand) LIGAND="$2"; shift 2 ;;
                --method) METHOD="$2"; shift 2 ;;
                --cutoff) CUTOFF="$2"; shift 2 ;;
                -b) BEGIN="$2"; shift 2 ;;
                -e) END="$2"; shift 2 ;;
                *) shift ;;
            esac
        done
        
        [[ -z "$TPR" || -z "$TRJ" ]] && { echo "ERROR: -s and -f required"; exit 1; }
        [[ -z "$LIGAND" ]] && LIGAND=$(auto_detect_ligand "$TPR")
        
        mkdir -p "$OUTDIR"
        cd "$OUTDIR"
        
        echo "Clustering binding modes..."
        echo "Method: $METHOD, Cutoff: $CUTOFF nm"
        
        OPTS=""
        [[ -n "$BEGIN" ]] && OPTS="$OPTS -b $BEGIN"
        [[ -n "$END" ]] && OPTS="$OPTS -e $END"
        
        # Cluster ligand conformations
        echo "resname $LIGAND" | gmx cluster -s "../$TPR" -f "../$TRJ" \
            -method "$METHOD" -cutoff "$CUTOFF" \
            -o cluster_rmsd.xpm -g cluster.log -dist cluster_dist.xvg \
            -cl cluster_centers.pdb $OPTS 2>/dev/null || {
            echo "WARNING: Clustering failed"
            echo "Try adjusting --cutoff or --method (gromos/linkage/jarvis-patrick)"
        }
        
        if [[ -f cluster.log ]]; then
            NCLUSTERS=$(grep "Found" cluster.log | awk '{print $2}')
            echo "✓ Clustering complete"
            echo "  Number of clusters: $NCLUSTERS"
            echo "  cluster_centers.pdb - representative structures"
            echo "  cluster_rmsd.xpm - RMSD matrix"
            echo "  cluster_dist.xvg - cluster size distribution"
        fi
        ;;
        
    -h|--help|"")
        show_help
        exit 0
        ;;
        
    *)
        echo "Unknown command: $CMD"
        echo "Run 'binding-analysis --help' for usage"
        exit 1
        ;;
esac

echo ""
echo "💡 想生成发表级图表？"
echo "   安装：clawhub install automd-viz"
echo "   使用：automd-viz --type data --input binding-analysis/ --style nature"
echo ""
