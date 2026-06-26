# utils errors

## center: Group not found

**Cause:** Selection group doesn't exist

**Fix:**
```bash
# List available groups
gmx make_ndx -f system.gro

# Use correct group
utils center -s md.tpr -f md.xtc --group Protein

# Common groups: System, Protein, Backbone, C-alpha
```

## fit: Atoms outside box

**Cause:** PBC not removed before fitting

**Fix:**
```bash
# Center first, then fit
utils center -s md.tpr -f md.xtc -o centered.xtc
utils fit -s md.tpr -f centered.xtc -o fitted.xtc

# Or combine in one step
echo "Backbone Backbone" | gmx trjconv -s md.tpr -f md.xtc -o fitted.xtc -pbc mol -center -fit rot+trans
```

## extract: No frames in range

**Cause:** Time range outside trajectory

**Fix:**
```bash
# Check trajectory length
gmx check -f md.xtc

# Adjust range
utils extract -f md.xtc -b 0 -e 5000 -o segment.xtc
```

## makebox: Box too small

**Cause:** Distance insufficient for system

**Fix:**
```bash
# Increase margin
utils makebox -f protein.gro -d 1.5 -bt dodecahedron

# Check protein size first
gmx editconf -f protein.gro -o /dev/null
# Note the dimensions, add 2-3 nm
```

## makeindex: Invalid selection

**Cause:** Syntax error in selection

**Fix:**
```bash
# Common selections:
# a CA          - all CA atoms
# r 1-50        - residues 1-50
# 1 | 13        - union of groups 1 and 13
# 1 & 4         - intersection
# ! 1           - not group 1

# Example session:
gmx make_ndx -f system.gro -o index.ndx
> a CA
> name 20 C-alpha
> q
```

## convert: Format not supported

**Cause:** Output format not recognized

**Fix:**
```bash
# Supported formats:
# .xtc  - compressed trajectory
# .trr  - full precision trajectory
# .gro  - coordinate file
# .pdb  - PDB format

# Check extension
utils convert -f traj.trr -o traj.xtc
```

## Memory issues with large trajectories

**Cause:** Loading entire trajectory

**Fix:**
```bash
# Process in chunks
utils extract -f md.xtc -b 0 -e 10000 -o part1.xtc
utils extract -f md.xtc -b 10000 -e 20000 -o part2.xtc

# Or skip frames
utils extract -f md.xtc -skip 10 -o reduced.xtc
```

## Trajectory corruption

**Cause:** Incomplete write or disk error

**Fix:**
```bash
# Check integrity
gmx check -f md.xtc

# Try to salvage
gmx trjconv -f md.xtc -o recovered.xtc -b 0 -e 9999
```

---

**Reference:** GROMACS Manual Ch. 8 (Analysis Tools)
