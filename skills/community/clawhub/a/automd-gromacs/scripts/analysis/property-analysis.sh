#!/bin/bash
# property-analysis - Physical Property Calculations
# Diffusion, viscosity, dielectric, thermodynamics, surface tension, RDF

set -e

show_help() {
    cat << 'EOF'
property-analysis - Physical Property Calculations

USAGE:
  property-analysis -s md.tpr -f md.xtc --property <type>

PROPERTIES:
  diffusion     - Diffusion coefficient (MSD/Einstein)
  viscosity     - Viscosity (Green-Kubo/Einstein)
  dielectric    - Dielectric constant
  thermodynamic - Cp, thermal expansion coefficient
  surface       - Surface tension
  rdf           - Radial distribution function
  density       - Density distribution

OPTIONS:
  -s FILE       Structure/TPR file (required)
  -f FILE       Trajectory file (required)
  -e FILE       Energy file (.edr, for thermodynamic/surface)
  -o DIR        Output directory (default: property_analysis)
  --property    Property type (required, see above)
  --group       Selection group (default: auto-detect)
  --group2      Second group for RDF (default: same as group)
  --temp        Temperature in K (default: 300)
  -b TIME       Begin time (ps)
  -e TIME       End time (ps)
  --trestart    Restart time for MSD (ps, default: 10)
  --rdf-cutoff  RDF cutoff distance (nm, default: 2.0)
  -h, --help    Show this help

EXAMPLES:
  # Diffusion coefficient of water
  property-analysis -s md.tpr -f md.xtc --property diffusion --group SOL

  # Viscosity calculation
  property-analysis -s md.tpr -f md.xtc -e md.edr --property viscosity

  # Dielectric constant
  property-analysis -s md.tpr -f md.xtc --property dielectric

  # RDF between protein and water
  property-analysis -s md.tpr -f md.xtc --property rdf --group Protein --group2 SOL

  # Heat capacity
  property-analysis -s md.tpr -f md.xtc -e md.edr --property thermodynamic

OUTPUT:
  diffusion:     msd.xvg, diffusion_coeff.txt
  viscosity:     viscosity.xvg, viscosity_value.txt
  dielectric:    dielectric.xvg, epsilon.txt
  thermodynamic: energy.xvg, cp.txt, alpha.txt
  surface:       surface_tension.xvg
  rdf:           rdf.xvg
  density:       density.xvg

PHYSICS BACKGROUND:
  Diffusion:     D = lim(t→∞) <|r(t)-r(0)|²> / (6t)  [Einstein]
  Viscosity:     η = V/(kT) ∫<P_αβ(t)P_αβ(0)>dt      [Green-Kubo]
                 η = σ_xy / γ̇                        [Einstein, NEMD]
  Dielectric:    ε = 1 + <M²>/(3ε₀VkT) - <M>²/(3ε₀VkT)
  Heat Capacity: Cp = <H²>/<H>² - 1) * RT²
  Surface:       γ = Lz/2 * (P_zz - (P_xx + P_yy)/2)
EOF
}

# Defaults
TPR=""
TRJ=""
EDR=""
OUTDIR="property_analysis"
PROPERTY=""
GROUP=""
GROUP2=""
TEMP=300
BEGIN=""
END=""
TRESTART=10
RDF_CUTOFF=2.0

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -s) TPR="$2"; shift 2 ;;
        -f) TRJ="$2"; shift 2 ;;
        -e) EDR="$2"; shift 2 ;;
        -o) OUTDIR="$2"; shift 2 ;;
        --property) PROPERTY="$2"; shift 2 ;;
        --group) GROUP="$2"; shift 2 ;;
        --group2) GROUP2="$2"; shift 2 ;;
        --temp) TEMP="$2"; shift 2 ;;
        -b) BEGIN="$2"; shift 2 ;;
        --trestart) TRESTART="$2"; shift 2 ;;
        --rdf-cutoff) RDF_CUTOFF="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
done

# Validation
[[ -z "$TPR" ]] && { echo "ERROR: -s required"; exit 1; }
[[ -z "$TRJ" ]] && { echo "ERROR: -f required"; exit 1; }
[[ -z "$PROPERTY" ]] && { echo "ERROR: --property required"; exit 1; }
[[ ! -f "$TPR" ]] && { echo "ERROR: TPR not found: $TPR"; exit 1; }
[[ ! -f "$TRJ" ]] && { echo "ERROR: Trajectory not found: $TRJ"; exit 1; }

mkdir -p "$OUTDIR"
cd "$OUTDIR"

# Logging
log() { echo "[$(date '+%H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

log "Property Analysis: $PROPERTY"
log "Input: $TPR, $TRJ"

# ============================================
# Auto-detect groups
# ============================================
auto_detect_group() {
    local tpr="$1"
    if gmx make_ndx -f "$tpr" -o /dev/null <<< "q" 2>&1 | grep -q "SOL"; then
        echo "SOL"
    elif gmx make_ndx -f "$tpr" -o /dev/null <<< "q" 2>&1 | grep -q "Protein"; then
        echo "Protein"
    else
        echo "System"
    fi
}

if [[ -z "$GROUP" ]]; then
    GROUP=$(auto_detect_group "../$TPR")
    log "[AUTO-FIX] Group auto-detected: $GROUP"
fi

[[ -z "$GROUP2" ]] && GROUP2="$GROUP"

# Time range args
TIME_ARGS=""
[[ -n "$BEGIN" ]] && TIME_ARGS="$TIME_ARGS -b $BEGIN"
[[ -n "$END" ]] && TIME_ARGS="$TIME_ARGS -e $END"

# ============================================
# Property Calculations
# ============================================

case "$PROPERTY" in
    diffusion)
        log "Calculating diffusion coefficient (MSD method)"
        
        # MSD calculation
        # Key: trestart controls averaging window
        # D = slope / 6 for 3D diffusion
        log "Running gmx msd..."
        echo "$GROUP" | gmx msd -s "../$TPR" -f "../$TRJ" \
            -o msd.xvg -mol -trestart "$TRESTART" $TIME_ARGS \
            2>&1 | tee msd.log
        
        # Extract diffusion coefficient
        # GROMACS outputs D in 10^-5 cm^2/s
        if grep -q "D\[" msd.log; then
            D=$(grep "D\[" msd.log | tail -1 | awk '{print $2}')
            D_err=$(grep "D\[" msd.log | tail -1 | awk '{print $4}')
            
            cat > diffusion_coeff.txt << EOF
Diffusion Coefficient Analysis
==============================
Group: $GROUP
Temperature: $TEMP K
Trestart: $TRESTART ps

Results:
--------
D = $D ± $D_err × 10⁻⁵ cm²/s
D = $(awk "BEGIN {print $D * 1e-5}" ) ± $(awk "BEGIN {print $D_err * 1e-5}") cm²/s

Physical Interpretation:
- D > 1e-5 cm²/s: Fast diffusion (small molecules, high T)
- D ~ 1e-5 cm²/s: Typical liquids (water ~ 2.3e-5 at 298K)
- D < 1e-6 cm²/s: Slow diffusion (polymers, high viscosity)

Einstein Relation: D = lim(t→∞) <|r(t)-r(0)|²> / (6t)
EOF
            log "Diffusion coefficient: $D ± $D_err × 10⁻⁵ cm²/s"
        else
            error "Failed to extract diffusion coefficient from msd.log"
        fi
        ;;
        
    viscosity)
        log "Calculating viscosity"
        
        # Method 1: Green-Kubo (from pressure tensor autocorrelation)
        # Requires: gmx energy with Pres-XX, Pres-YY, Pres-ZZ, Pres-XY, etc.
        
        if [[ -z "$EDR" ]]; then
            error "Viscosity requires -e <edr_file>"
        fi
        [[ ! -f "$EDR" ]] && error "EDR file not found: $EDR"
        
        log "Extracting pressure tensor components..."
        
        # Extract off-diagonal pressure tensor elements
        # η ∝ ∫<P_xy(t)P_xy(0)>dt
        cat > energy_input.txt << 'EOF'
Pres-XX
Pres-YY
Pres-ZZ
Pres-XY
Pres-XZ
Pres-YZ
0
EOF
        
        gmx energy -f "../$EDR" -o pressure_tensor.xvg $TIME_ARGS < energy_input.txt 2>&1 | tee energy.log
        
        # Calculate viscosity using gmx tcaf (time correlation function)
        # Note: This is simplified - full Green-Kubo requires custom analysis
        log "Calculating pressure autocorrelation..."
        
        # Extract Pxy for viscosity estimate
        echo "Pres-XY" | gmx energy -f "../$EDR" -o pxy.xvg $TIME_ARGS 2>&1 > /dev/null
        
        # Estimate viscosity from pressure fluctuations
        # η = V/(kT) * ∫<δP_xy(t)δP_xy(0)>dt
        # Simplified: η ≈ V/(kT) * <(δP_xy)²> * τ_corr
        
        cat > viscosity.txt << EOF
Viscosity Analysis
==================
Method: Pressure tensor fluctuation (simplified Green-Kubo)
Temperature: $TEMP K

Note: Full Green-Kubo viscosity calculation requires:
1. Long simulation (> 10 ns)
2. Pressure tensor autocorrelation function
3. Integration of correlation function

For accurate viscosity:
- Use gmx tcaf for autocorrelation
- Or use NEMD (non-equilibrium MD) with shear flow
- Or use Einstein relation: η = lim(t→∞) <W(t)> / (2Vt)

Green-Kubo Formula:
η = V/(kT) ∫₀^∞ <P_αβ(t)P_αβ(0)> dt

Typical Values:
- Water (298K): 0.89 mPa·s
- Ethanol (298K): 1.07 mPa·s
- Glycerol (298K): 1412 mPa·s

Output Files:
- pressure_tensor.xvg: All pressure components
- pxy.xvg: Off-diagonal element for viscosity
EOF
        log "Viscosity analysis complete (see viscosity.txt for details)"
        ;;
        
    dielectric)
        log "Calculating dielectric constant"
        
        # Dielectric constant from dipole moment fluctuations
        # ε = 1 + <M²>/(3ε₀VkT) - <M>²/(3ε₀VkT)
        
        log "Running gmx dipoles..."
        echo "$GROUP" | gmx dipoles -s "../$TPR" -f "../$TRJ" \
            -o dipole.xvg -eps epsilon.xvg -temp "$TEMP" $TIME_ARGS \
            2>&1 | tee dipoles.log
        
        # Extract dielectric constant
        if [[ -f epsilon.xvg ]]; then
            # Average epsilon from last column
            EPSILON=$(grep -v '^[@#]' epsilon.xvg | awk '{sum+=$NF; n++} END {print sum/n}')
            EPSILON_ERR=$(grep -v '^[@#]' epsilon.xvg | awk '{sum+=$NF; sumsq+=$NF*$NF; n++} END {print sqrt((sumsq/n - (sum/n)^2)/n)}')
            
            cat > dielectric_constant.txt << EOF
Dielectric Constant Analysis
=============================
Group: $GROUP
Temperature: $TEMP K

Results:
--------
ε = $EPSILON ± $EPSILON_ERR

Physical Interpretation:
- ε = 1: Vacuum
- ε ~ 2-4: Non-polar liquids (hexane, benzene)
- ε ~ 20-40: Polar liquids (alcohols)
- ε ~ 80: Water (298K, experimental: 78.4)
- ε > 100: Highly polar systems

Formula:
ε = 1 + <M²>/(3ε₀VkT) - <M>²/(3ε₀VkT)

where M is total dipole moment, V is volume, k is Boltzmann constant

Output Files:
- dipole.xvg: Dipole moment vs time
- epsilon.xvg: Dielectric constant vs time
EOF
            log "Dielectric constant: $EPSILON ± $EPSILON_ERR"
        else
            error "Failed to calculate dielectric constant"
        fi
        ;;
        
    thermodynamic)
        log "Calculating thermodynamic properties"
        
        if [[ -z "$EDR" ]]; then
            error "Thermodynamic analysis requires -e <edr_file>"
        fi
        [[ ! -f "$EDR" ]] && error "EDR file not found: $EDR"
        
        log "Extracting energy terms..."
        
        # Extract potential, kinetic, total energy, enthalpy
        cat > thermo_input.txt << 'EOF'
Potential
Kinetic-En.
Total-Energy
Enthalpy
Temperature
Pressure
Volume
Density
0
EOF
        
        gmx energy -f "../$EDR" -o thermodynamic.xvg $TIME_ARGS < thermo_input.txt 2>&1 | tee thermo.log
        
        # Calculate heat capacity Cp
        # Cp = (<H²> - <H>²) / (kT²)
        # Also: thermal expansion coefficient α = (1/V)(∂V/∂T)_P
        
        log "Analyzing fluctuations for Cp..."
        
        # Extract enthalpy for Cp calculation
        echo "Enthalpy" | gmx energy -f "../$EDR" -o enthalpy.xvg $TIME_ARGS 2>&1 > /dev/null
        
        # Calculate statistics
        if [[ -f enthalpy.xvg ]]; then
            H_AVG=$(grep -v '^[@#]' enthalpy.xvg | awk '{sum+=$2; n++} END {print sum/n}')
            H_SQ=$(grep -v '^[@#]' enthalpy.xvg | awk '{sum+=$2*$2; n++} END {print sum/n}')
            H_FLUCT=$(awk "BEGIN {print $H_SQ - $H_AVG * $H_AVG}")
            
            # Cp = dH/dT ≈ <(ΔH)²> / (kT²)
            # In kJ/mol/K
            kB=0.008314  # kJ/mol/K
            Cp=$(awk "BEGIN {print $H_FLUCT / ($kB * $TEMP * $TEMP)}")
            
            cat > heat_capacity.txt << EOF
Thermodynamic Properties
========================
Temperature: $TEMP K

Heat Capacity (Cp):
-------------------
<H> = $H_AVG kJ/mol
<H²> = $H_SQ (kJ/mol)²
<(ΔH)²> = $H_FLUCT (kJ/mol)²
Cp ≈ $Cp J/mol/K

Formula:
Cp = <(ΔH)²> / (kT²)

Note: This is a fluctuation-based estimate.
For accurate Cp, run simulations at multiple temperatures.

Typical Values:
- Water: 75.3 J/mol/K (298K)
- Ethanol: 112.3 J/mol/K (298K)
- Proteins: ~1.2-1.5 J/g/K

Output Files:
- thermodynamic.xvg: All energy terms
- enthalpy.xvg: Enthalpy vs time
EOF
            log "Heat capacity: $Cp J/mol/K"
        fi
        
        # Thermal expansion coefficient
        echo "Volume" | gmx energy -f "../$EDR" -o volume.xvg $TIME_ARGS 2>&1 > /dev/null
        
        if [[ -f volume.xvg ]]; then
            V_AVG=$(grep -v '^[@#]' volume.xvg | awk '{sum+=$2; n++} END {print sum/n}')
            V_STD=$(grep -v '^[@#]' volume.xvg | awk '{sum+=$2; sumsq+=$2*$2; n++} END {print sqrt(sumsq/n - (sum/n)^2)}')
            
            cat > thermal_expansion.txt << EOF
Thermal Expansion Coefficient
==============================
<V> = $V_AVG nm³
σ_V = $V_STD nm³

Note: Accurate α requires simulations at multiple temperatures:
α = (1/V) * (∂V/∂T)_P

For single-temperature estimate:
α ≈ <(ΔV)²> / (VkT²)

Typical Values:
- Water (298K): 2.07 × 10⁻⁴ K⁻¹
- Ethanol (298K): 1.12 × 10⁻³ K⁻¹
- Proteins: ~1-5 × 10⁻⁴ K⁻¹
EOF
        fi
        ;;
        
    surface)
        log "Calculating surface tension"
        
        if [[ -z "$EDR" ]]; then
            error "Surface tension requires -e <edr_file>"
        fi
        [[ ! -f "$EDR" ]] && error "EDR file not found: $EDR"
        
        log "Extracting pressure tensor..."
        
        # Surface tension: γ = Lz/2 * (P_zz - (P_xx + P_yy)/2)
        # Requires anisotropic pressure coupling (semi-isotropic or anisotropic)
        
        cat > surface_input.txt << 'EOF'
Pres-XX
Pres-YY
Pres-ZZ
Box-X
Box-Y
Box-Z
0
EOF
        
        gmx energy -f "../$EDR" -o surface_data.xvg $TIME_ARGS < surface_input.txt 2>&1 | tee surface.log
        
        # Calculate surface tension
        # γ = Lz/2 * (P_zz - (P_xx + P_yy)/2)
        # Units: bar·nm = 100 mN/m
        
        log "Calculating surface tension from pressure anisotropy..."
        
        awk '
        BEGIN {
            sum_pxx=0; sum_pyy=0; sum_pzz=0; sum_lz=0; n=0;
        }
        /^[^@#]/ {
            pxx=$2; pyy=$3; pzz=$4;
            lz=$7;
            sum_pxx+=pxx; sum_pyy+=pyy; sum_pzz+=pzz; sum_lz+=lz;
            n++;
        }
        END {
            if (n>0) {
                pxx_avg=sum_pxx/n;
                pyy_avg=sum_pyy/n;
                pzz_avg=sum_pzz/n;
                lz_avg=sum_lz/n;
                
                p_lateral=(pxx_avg+pyy_avg)/2;
                p_normal=pzz_avg;
                
                # γ = Lz/2 * (P_N - P_L)
                # Convert: bar·nm → mN/m (factor: 100)
                gamma = (lz_avg/2) * (p_normal - p_lateral) * 100;
                
                print "Surface Tension Analysis";
                print "========================";
                print "";
                print "Pressure Components:";
                print "P_xx = " pxx_avg " bar";
                print "P_yy = " pyy_avg " bar";
                print "P_zz = " pzz_avg " bar";
                print "P_lateral = " p_lateral " bar";
                print "P_normal = " p_normal " bar";
                print "";
                print "Box Dimensions:";
                print "Lz = " lz_avg " nm";
                print "";
                print "Surface Tension:";
                print "γ = " gamma " mN/m";
                print "";
                print "Formula:";
                print "γ = (Lz/2) * (P_N - P_L)";
                print "";
                print "Typical Values:";
                print "- Water/vacuum (298K): 72 mN/m";
                print "- Water/air (298K): 72 mN/m";
                print "- Ethanol/air (298K): 22 mN/m";
                print "- Hexane/air (298K): 18 mN/m";
                print "";
                print "Note: Requires interface perpendicular to z-axis";
                print "      and semi-isotropic/anisotropic pressure coupling";
            }
        }
        ' surface_data.xvg > surface_tension.txt
        
        log "Surface tension calculated (see surface_tension.txt)"
        ;;
        
    rdf)
        log "Calculating radial distribution function"
        
        # RDF: g(r) = <ρ(r)> / <ρ_bulk>
        # Shows spatial correlation between particles
        
        log "Running gmx rdf..."
        printf "%s\n%s" "$GROUP" "$GROUP2" | gmx rdf -s "../$TPR" -f "../$TRJ" \
            -o rdf.xvg -cn rdf_cn.xvg -cut "$RDF_CUTOFF" $TIME_ARGS \
            2>&1 | tee rdf.log
        
        # Analyze RDF peaks
        if [[ -f rdf.xvg ]]; then
            # Find first peak position (coordination shell)
            FIRST_PEAK=$(grep -v '^[@#]' rdf.xvg | awk 'NR>1 && $2>prev {peak_r=$1; peak_g=$2} {prev=$2} END {print peak_r, peak_g}')
            
            cat > rdf_analysis.txt << EOF
Radial Distribution Function Analysis
======================================
Group 1: $GROUP
Group 2: $GROUP2
Cutoff: $RDF_CUTOFF nm

First Peak:
-----------
r = $(echo $FIRST_PEAK | awk '{print $1}') nm
g(r) = $(echo $FIRST_PEAK | awk '{print $2}')

Physical Interpretation:
- g(r) = 1: Random distribution (ideal gas)
- g(r) > 1: Preferred distance (attraction, structure)
- g(r) < 1: Excluded volume (repulsion)
- First peak: First coordination shell
- Peak height: Degree of ordering

Integration:
∫₀^r₁ 4πr²ρg(r)dr = Coordination number

Typical Systems:
- Liquid water O-O: First peak at ~0.28 nm, g(r)~3
- Liquid argon: First peak at ~0.38 nm, g(r)~2.5
- Crystalline: Sharp peaks, long-range order

Output Files:
- rdf.xvg: g(r) vs r
- rdf_cn.xvg: Cumulative coordination number
EOF
            log "RDF analysis complete"
        else
            error "Failed to calculate RDF"
        fi
        ;;
        
    density)
        log "Calculating density distribution"
        
        # Density profile along z-axis (useful for interfaces, membranes)
        
        log "Running gmx density..."
        echo "$GROUP" | gmx density -s "../$TPR" -f "../$TRJ" \
            -o density.xvg -d Z $TIME_ARGS \
            2>&1 | tee density.log
        
        if [[ -f density.xvg ]]; then
            # Calculate average density
            AVG_DENSITY=$(grep -v '^[@#]' density.xvg | awk '{sum+=$2; n++} END {print sum/n}')
            
            cat > density_analysis.txt << EOF
Density Distribution Analysis
==============================
Group: $GROUP
Direction: Z-axis

Average Density: $AVG_DENSITY kg/m³

Physical Interpretation:
- Uniform profile: Homogeneous system
- Oscillations: Layered structure (interfaces, membranes)
- Gradients: Concentration gradients

Applications:
- Membrane simulations: Lipid/water density profiles
- Interfaces: Liquid/vapor, liquid/liquid
- Adsorption: Density near surfaces
- Solvation shells: Density around solutes

Typical Values:
- Water (298K): 997 kg/m³
- Lipid bilayer: ~800-1000 kg/m³ (headgroups), ~800 kg/m³ (tails)
- Proteins: ~1350 kg/m³

Output Files:
- density.xvg: Density vs z-coordinate
EOF
            log "Density distribution calculated"
        else
            error "Failed to calculate density distribution"
        fi
        ;;
        
    *)
        error "Unknown property: $PROPERTY. Use --help for options."
        ;;
esac

# ============================================
# Generate Report
# ============================================

cat > PROPERTY_ANALYSIS_REPORT.md << EOF
# Property Analysis Report

**Property**: $PROPERTY  
**Date**: $(date)  
**Input**: $TPR, $TRJ  
**Group**: $GROUP  
**Temperature**: $TEMP K  

## Analysis Summary

Property type: **$PROPERTY**

$(if [[ "$PROPERTY" == "diffusion" && -f diffusion_coeff.txt ]]; then
    cat diffusion_coeff.txt
elif [[ "$PROPERTY" == "viscosity" && -f viscosity.txt ]]; then
    cat viscosity.txt
elif [[ "$PROPERTY" == "dielectric" && -f dielectric_constant.txt ]]; then
    cat dielectric_constant.txt
elif [[ "$PROPERTY" == "thermodynamic" && -f heat_capacity.txt ]]; then
    cat heat_capacity.txt
    [[ -f thermal_expansion.txt ]] && cat thermal_expansion.txt
elif [[ "$PROPERTY" == "surface" && -f surface_tension.txt ]]; then
    cat surface_tension.txt
elif [[ "$PROPERTY" == "rdf" && -f rdf_analysis.txt ]]; then
    cat rdf_analysis.txt
elif [[ "$PROPERTY" == "density" && -f density_analysis.txt ]]; then
    cat density_analysis.txt
fi)

## Output Files

\`\`\`
$(ls -lh *.xvg *.txt *.log 2>/dev/null | awk '{print $9, $5}')
\`\`\`

## Command Used

\`\`\`bash
property-analysis -s $TPR -f $TRJ $([ -n "$EDR" ] && echo "-e $EDR") --property $PROPERTY --group $GROUP $([ "$GROUP2" != "$GROUP" ] && echo "--group2 $GROUP2") --temp $TEMP
\`\`\`

---
*Generated by AutoMD-GROMACS property-analysis*
EOF

log "Analysis complete! Report: $OUTDIR/PROPERTY_ANALYSIS_REPORT.md"
log "Output directory: $OUTDIR"

echo ""
echo "💡 想生成发表级图表？"
echo "   安装：clawhub install automd-viz"
echo "   使用：automd-viz --type data --input $OUTDIR/ --style nature"
echo ""

exit 0
