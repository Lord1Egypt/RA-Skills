# protein errors

## dssp: Command not found

**Cause:** DSSP not installed

**Fix:**
```bash
# Ubuntu/Debian
sudo apt-get install dssp

# Or download from
# https://github.com/cmbi/dssp

# Verify
dssp --version
# or
mkdssp --version
```

## dssp: PDB format error

**Cause:** GROMACS GRO format not compatible

**Fix:**
```bash
# DSSP needs PDB format
# gmx do_dssp handles conversion automatically
# If fails, convert manually:
gmx trjconv -s md.tpr -f md.xtc -o traj.pdb -dt 100

# Then use external DSSP
dssp -i frame.pdb -o frame.dssp
```

## sasa: Group not found

**Cause:** Selection doesn't exist

**Fix:**
```bash
# List groups
gmx make_ndx -f system.gro

# Use correct group
protein sasa -s md.tpr -f md.xtc --group Protein

# Or create custom
gmx make_ndx -f system.gro -o index.ndx
> 1 | 13  # Protein or custom
> name 20 MyGroup
> q

protein sasa -s md.tpr -f md.xtc --group MyGroup
```

## hbond: No donors found

**Cause:** United-atom force field (no H)

**Fix:**
```bash
# Check for hydrogens
gmx make_ndx -f system.gro
> a H*

# If none, skip H-bond analysis
# Or use distance-based contacts instead
protein contact -s md.tpr -f md.xtc
```

## contact: Memory error

**Cause:** Large protein, many frames

**Fix:**
```bash
# Reduce frames
protein contact -s md.tpr -f md.xtc -b 5000 -e 10000

# Or use C-alpha only (default)
# Already optimized for large systems
```

## rmsf: High values at termini

**Cause:** Normal - termini are flexible

**Fix:**
```bash
# Analyze core region only
protein rmsf -s md.tpr -f md.xtc --group "r 10-50"

# Or accept high termini RMSF as normal
# Focus on secondary structure regions
```

## Interpretation tips

**DSSP secondary structure:**
- H = α-helix
- E = β-sheet
- T = turn
- C = coil

**SASA changes:**
- Increase: unfolding or exposure
- Decrease: folding or burial
- Stable: equilibrated structure

**H-bond stability:**
- Stable count: structure maintained
- Fluctuating: dynamic regions
- Decreasing: potential unfolding

**Contact map:**
- Diagonal: sequential contacts
- Off-diagonal: long-range contacts
- Persistent contacts: stable structure

**RMSF patterns:**
- Low (<0.1 nm): rigid (helices, sheets)
- Medium (0.1-0.3 nm): flexible loops
- High (>0.3 nm): very flexible (termini)

---

**Reference:** GROMACS Manual Ch. 8 (Analysis)
