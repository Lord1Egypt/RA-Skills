# Property Analysis Troubleshooting Guide

## Common Errors and Solutions

### ERROR-001: Missing Input Files
**Symptom**: `ERROR: TPR not found` or `ERROR: Trajectory not found`

**Cause**: Input files not specified or incorrect path

**Fix**:
```bash
# Check file existence
ls -lh md.tpr md.xtc

# Use absolute paths if needed
property-analysis -s /path/to/md.tpr -f /path/to/md.xtc --property diffusion
```

---

### ERROR-002: Property Type Not Specified
**Symptom**: `ERROR: --property required`

**Cause**: Missing `--property` argument

**Fix**:
```bash
# Specify property type
property-analysis -s md.tpr -f md.xtc --property diffusion

# Available properties:
# diffusion, viscosity, dielectric, thermodynamic, surface, rdf, density
```

---

### ERROR-003: EDR File Required
**Symptom**: `ERROR: Viscosity requires -e <edr_file>` or `Thermodynamic analysis requires -e <edr_file>`

**Cause**: Energy file (.edr) not provided for properties that need it

**Fix**:
```bash
# Provide energy file
property-analysis -s md.tpr -f md.xtc -e md.edr --property viscosity

# Properties requiring EDR:
# - viscosity
# - thermodynamic
# - surface
```

**Prevention**: Always save .edr file during mdrun:
```bash
gmx mdrun -deffnm md  # Generates md.edr automatically
```

---

### ERROR-004: Group Selection Failed
**Symptom**: `Group <name> not found` or selection prompt hangs

**Cause**: Specified group doesn't exist in system

**Fix**:
```bash
# Check available groups
gmx make_ndx -f md.tpr -o index.ndx
# Type 'q' to see all groups

# Use auto-detection (default)
property-analysis -s md.tpr -f md.xtc --property diffusion
# Auto-detects: SOL > Protein > System

# Or specify correct group
property-analysis -s md.tpr -f md.xtc --property diffusion --group SOL
```

**Common Group Names**:
- `System`: Entire system
- `Protein`: Protein atoms
- `SOL`: Water molecules
- `NA`, `CL`: Ions
- `Backbone`, `C-alpha`: Protein subsets

---

### ERROR-005: Diffusion Coefficient Extraction Failed
**Symptom**: `Failed to extract diffusion coefficient from msd.log`

**Cause**: 
1. Trajectory too short (< 1 ns)
2. MSD not linear (system not equilibrated)
3. Wrong group selected (immobile atoms)

**Fix**:
```bash
# 1. Use longer trajectory
property-analysis -s md.tpr -f md.xtc --property diffusion -b 5000 -e 15000
# Skip first 5 ns (equilibration)

# 2. Adjust trestart (averaging window)
property-analysis -s md.tpr -f md.xtc --property diffusion --trestart 20
# Default: 10 ps, increase for noisy data

# 3. Select mobile group
property-analysis -s md.tpr -f md.xtc --property diffusion --group SOL
# Water diffuses, protein doesn't
```

**Diagnosis**:
```bash
# Check MSD linearity
xmgrace msd.xvg
# Should be linear after initial ballistic regime (~1 ps)
```

**Expected Values**:
- Water (298K): D ~ 2.3 × 10⁻⁵ cm²/s
- Small molecules: D ~ 0.5-5 × 10⁻⁵ cm²/s
- Proteins: D ~ 0.01-0.1 × 10⁻⁵ cm²/s

---

### ERROR-006: Viscosity Calculation Incomplete
**Symptom**: `viscosity.txt` says "requires custom analysis"

**Cause**: Full Green-Kubo viscosity needs pressure autocorrelation integration (not automated in GROMACS)

**Fix**:

**Option 1**: Use NEMD (Non-Equilibrium MD) - see `non-equilibrium` skill:
```bash
# Run shear flow simulation
non-equilibrium -s md.tpr -f md.xtc --nemd-type deform --deform-rate 0.001
# Directly calculates η = σ_xy / γ̇
```

**Option 2**: Manual Green-Kubo calculation:
```bash
# 1. Extract pressure tensor
property-analysis -s md.tpr -f md.xtc -e md.edr --property viscosity
# Generates pxy.xvg

# 2. Calculate autocorrelation
gmx analyze -f pxy.xvg -ac pxy_acf.xvg

# 3. Integrate ACF
# η = V/(kT) * ∫<P_xy(t)P_xy(0)>dt
# Use numerical integration (trapz, scipy, etc.)
```

**Option 3**: Use literature force field values:
- OPLS-AA water: η ~ 0.85 mPa·s (298K)
- TIP3P water: η ~ 0.32 mPa·s (298K, underestimates)
- TIP4P/2005: η ~ 0.855 mPa·s (298K, accurate)

---

### ERROR-007: Dielectric Constant Too Low/High
**Symptom**: ε << 1 or ε >> 1000

**Cause**:
1. Wrong group selected (non-polar molecules)
2. Trajectory too short (< 10 ns for convergence)
3. System too small (< 1000 molecules)
4. Cutoff artifacts

**Fix**:
```bash
# 1. Select polar molecules
property-analysis -s md.tpr -f md.xtc --property dielectric --group SOL
# Water should give ε ~ 80

# 2. Use longer trajectory
property-analysis -s md.tpr -f md.xtc --property dielectric -b 10000
# Skip first 10 ns

# 3. Check system size
gmx check -f md.tpr
# Need > 1000 water molecules for bulk properties

# 4. Verify simulation parameters (mdp)
# - rcoulomb >= 1.2 nm
# - PME for long-range electrostatics
# - No reaction-field (use PME)
```

**Expected Values**:
- Water (298K): ε ~ 78-80
- Methanol: ε ~ 33
- Ethanol: ε ~ 25
- Acetone: ε ~ 21
- Non-polar (hexane): ε ~ 2

---

### ERROR-008: Surface Tension Calculation Failed
**Symptom**: Unrealistic γ values (negative or > 1000 mN/m)

**Cause**:
1. No interface in system (bulk liquid)
2. Interface not perpendicular to z-axis
3. Isotropic pressure coupling (should be semi-isotropic)
4. System not equilibrated

**Fix**:
```bash
# 1. Verify interface setup
# System should have liquid/vapor or liquid/liquid interface
# Interface must be perpendicular to z-axis

# 2. Check pressure coupling in mdp
# pcoupl = Parrinello-Rahman
# pcoupltype = semi-isotropic  # NOT isotropic!
# ref_p = 1.0 1.0              # Pxy and Pz independent

# 3. Equilibrate interface (> 10 ns)
property-analysis -s md.tpr -f md.xtc -e md.edr --property surface -b 10000

# 4. Verify interface position
gmx density -s md.tpr -f md.xtc -d Z -o density_z.xvg
# Should see clear density drop at interface
```

**Expected Values**:
- Water/vacuum (298K): γ ~ 72 mN/m
- Ethanol/air: γ ~ 22 mN/m
- Hexane/air: γ ~ 18 mN/m
- Lipid bilayer: γ ~ 20-40 mN/m (depends on lipid)

---

### ERROR-009: RDF Shows No Structure
**Symptom**: g(r) ≈ 1 everywhere (flat line)

**Cause**:
1. Groups too far apart (no correlation)
2. Cutoff too small
3. System too dilute
4. Wrong groups selected

**Fix**:
```bash
# 1. Check group proximity
gmx mindist -s md.tpr -f md.xtc -od mindist.xvg
# Should have close contacts

# 2. Increase cutoff
property-analysis -s md.tpr -f md.xtc --property rdf --rdf-cutoff 3.0
# Default: 2.0 nm, increase to 3-4 nm

# 3. Select interacting groups
property-analysis -s md.tpr -f md.xtc --property rdf --group Protein --group2 SOL
# Protein-water RDF

# 4. Verify concentration
gmx energy -f md.edr -o density.xvg
# Check system density
```

**Typical RDF Features**:
- **Liquid water O-O**: First peak at 0.28 nm, g(r) ~ 3
- **Protein-water**: First peak at 0.18-0.20 nm (H-bonds)
- **Ion-water**: Sharp first peak at 0.20-0.25 nm
- **Gas phase**: g(r) = 1 (no structure)

---

### ERROR-010: Density Profile Noisy
**Symptom**: density.xvg shows large fluctuations

**Cause**:
1. Trajectory too short
2. Bin size too small (default)
3. System too small

**Fix**:
```bash
# 1. Use longer trajectory
property-analysis -s md.tpr -f md.xtc --property density -b 5000

# 2. Increase bin size (manual gmx density)
echo "System" | gmx density -s md.tpr -f md.xtc -d Z -o density.xvg -sl 100
# -sl 100: 100 slices (larger bins)

# 3. Average over multiple runs
# Concatenate trajectories: gmx trjcat -f run1.xtc run2.xtc -o combined.xtc
```

---

### ERROR-011: Heat Capacity Unrealistic
**Symptom**: Cp < 0 or Cp >> 1000 J/mol/K

**Cause**:
1. Trajectory too short (< 10 ns)
2. System not equilibrated
3. Fluctuation formula limitations (single-temperature)

**Fix**:
```bash
# 1. Use longer equilibrated trajectory
property-analysis -s md.tpr -f md.xtc -e md.edr --property thermodynamic -b 10000

# 2. Check equilibration
gmx energy -f md.edr -o energy.xvg
# Temperature, pressure, energy should be stable

# 3. For accurate Cp: Run multiple temperatures
# T = 290, 295, 300, 305, 310 K
# Cp = dH/dT (finite difference)
```

**Note**: Fluctuation-based Cp is approximate. For publication-quality:
- Run 5+ temperatures (ΔT = 5-10 K)
- Use finite difference: Cp = ΔH/ΔT
- Or use 2PT method (two-phase thermodynamics)

---

## Performance Issues

### ISSUE-001: Analysis Very Slow
**Symptom**: gmx commands take > 10 minutes

**Cause**: Large trajectory file or high frame rate

**Fix**:
```bash
# 1. Reduce trajectory size (skip frames)
gmx trjconv -s md.tpr -f md.xtc -o md_skip10.xtc -skip 10
# Keep every 10th frame

# 2. Use time range
property-analysis -s md.tpr -f md.xtc --property diffusion -b 5000 -e 10000
# Analyze 5-10 ns only

# 3. Reduce group size
echo "C-alpha" | gmx make_ndx -f md.tpr -o index.ndx
property-analysis -s md.tpr -f md.xtc --property diffusion --group C-alpha
# Fewer atoms = faster
```

---

### ISSUE-002: Out of Memory
**Symptom**: `Killed` or `Cannot allocate memory`

**Cause**: Large system + long trajectory

**Fix**:
```bash
# 1. Process in chunks
property-analysis -s md.tpr -f md.xtc --property diffusion -b 0 -e 50000
property-analysis -s md.tpr -f md.xtc --property diffusion -b 50000 -e 100000
# Analyze separately, then average

# 2. Use compressed trajectory
gmx trjconv -s md.tpr -f md.trr -o md.xtc
# .xtc is 10-20x smaller than .trr

# 3. Reduce precision
gmx trjconv -s md.tpr -f md.xtc -o md_prec3.xtc -ndec 3
# Default: 3 decimals, reduce to 2 if needed
```

---

## Validation Checks

### Check 1: Diffusion Coefficient Sanity
```bash
# Water at 298K should give D ~ 2.3 × 10⁻⁵ cm²/s
# If D < 0.1 or D > 10: Something is wrong

# Common issues:
# - D too low: System frozen, wrong group, too short trajectory
# - D too high: Vacuum, gas phase, numerical error
```

### Check 2: Dielectric Constant Convergence
```bash
# Plot epsilon.xvg
xmgrace epsilon.xvg

# Should converge after ~10 ns
# If still drifting: Extend simulation
```

### Check 3: RDF Normalization
```bash
# g(r) should approach 1.0 at large r (bulk limit)
# If g(r) → 0 or g(r) → constant ≠ 1: Normalization issue

# Check:
tail -20 rdf.xvg
# Last values should be ~1.0 ± 0.1
```

---

## Best Practices

1. **Equilibration**: Always skip first 5-10 ns (`-b 5000`)
2. **Trajectory Length**: 
   - Diffusion: > 10 ns
   - Viscosity: > 50 ns (Green-Kubo)
   - Dielectric: > 10 ns
   - RDF: > 5 ns
3. **System Size**:
   - Bulk properties: > 1000 molecules
   - Surface properties: > 5000 atoms
4. **Validation**: Compare with experimental values or literature
5. **Convergence**: Check time-dependent plots (not just averages)

---

## Quick Diagnostic Commands

```bash
# Check trajectory info
gmx check -f md.xtc

# Check system composition
gmx make_ndx -f md.tpr -o index.ndx
# Type 'q' to see groups

# Check energy terms available
gmx energy -f md.edr
# Type '0' to see all terms

# Verify equilibration
gmx energy -f md.edr -o temperature.xvg
# Plot and check stability

# Check box size (for cutoffs)
gmx check -f md.tpr
# Verify box > 2*cutoff
```

---

## Getting Help

If errors persist:

1. **Check GROMACS version**: `gmx --version`
   - Requires GROMACS 2020+
   - Some features need 2021+

2. **Verify input files**:
   ```bash
   gmx check -f md.tpr
   gmx check -f md.xtc
   gmx check -f md.edr
   ```

3. **Test with minimal system**:
   ```bash
   # Use short trajectory first
   property-analysis -s md.tpr -f md.xtc --property diffusion -b 0 -e 1000
   ```

4. **Consult GROMACS manual**:
   - Diffusion: `gmx help msd`
   - RDF: `gmx help rdf`
   - Dielectric: `gmx help dipoles`

5. **Check simulation parameters** (mdp file):
   - Cutoffs: rcoulomb, rvdw >= 1.0 nm
   - Electrostatics: PME (not cut-off)
   - Pressure coupling: Appropriate for property
   - Output frequency: nstxout-compressed <= 1000 (1 ps)

---

*Last updated: 2026-04-09*
