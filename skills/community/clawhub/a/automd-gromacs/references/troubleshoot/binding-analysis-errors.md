# Binding Analysis Troubleshooting Guide

## Common Errors and Solutions

### ERROR-001: gmx_MMPBSA not available
**Symptom**: MM-PBSA calculation fails with "gmx_MMPBSA not found"

**Cause**: gmx_MMPBSA package not installed

**Fix**:
```bash
pip install gmx_MMPBSA
```

**Alternative**: Use simplified interaction energy analysis (automatic fallback)

---

### ERROR-002: Ligand auto-detection failed
**Symptom**: "Cannot find ligand residue"

**Cause**: Ligand residue name not in common list (LIG, MOL, UNK, DRG, INH)

**Fix**: Specify ligand explicitly
```bash
binding-analysis mmpbsa -s md.tpr -f md.xtc --ligand "resname YOUR_LIGAND"
```

**Check ligand name**:
```bash
gmx dump -s md.tpr | grep "moltype\|residue"
```

---

### ERROR-003: Pocket identification failed
**Symptom**: "Pocket identification failed" or empty pocket_residues.ndx

**Cause**: 
- Ligand too far from protein (> 0.5 nm)
- Incorrect ligand selection
- Trajectory not properly centered

**Fix**:
1. Check ligand-protein distance:
```bash
echo "Protein resname LIG" | gmx mindist -s md.tpr -f md.xtc -od mindist.xvg
```

2. Center trajectory:
```bash
echo "Protein System" | gmx trjconv -s md.tpr -f md.xtc -o md_centered.xtc -center -pbc mol
```

3. Manual pocket selection:
```bash
gmx select -s md.tpr -select "same residue as (within 0.5 of resname LIG)"
```

---

### ERROR-004: H-bond analysis returns zero bonds
**Symptom**: Average H-bonds = 0.0

**Cause**:
- No hydrogen atoms in structure (united-atom force field)
- Incorrect group selection
- H-bond criteria too strict

**Fix**:
1. Check for hydrogens:
```bash
gmx dump -s md.tpr | grep " H " | head
```

2. Reconstruct hydrogens (if missing):
```bash
echo "System" | gmx trjconv -s md.tpr -f md.xtc -o md_h.xtc
# Note: This doesn't add hydrogens, just a workaround
```

3. Relax H-bond criteria:
```bash
# Default: -r 0.35 -a 30
echo "Protein LIG" | gmx hbond -s md.tpr -f md.xtc -num hbond.xvg -r 0.40 -a 35
```

---

### ERROR-005: Contact map generation failed
**Symptom**: "gmx mdmat failed" or empty contact_mean.xpm

**Cause**:
- Groups too large (memory issue)
- Trajectory too long
- Incorrect selections

**Fix**:
1. Reduce trajectory length:
```bash
binding-analysis interact -s md.tpr -f md.xtc -b 5000 -e 10000
```

2. Use smaller selections:
```bash
binding-analysis interact -s md.tpr -f md.xtc --protein "r 50-150" --ligand "resname LIG"
```

3. Increase contact threshold:
```bash
echo "Protein LIG" | gmx mdmat -s md.tpr -f md.xtc -mean contact.xpm -t 0.8
```

---

### ERROR-006: Clustering fails with "No structures found"
**Symptom**: Clustering returns 0 clusters

**Cause**:
- Cutoff too small (no structures within cutoff)
- Ligand RMSD too large
- Insufficient frames

**Fix**:
1. Increase cutoff:
```bash
binding-analysis cluster -s md.tpr -f md.xtc --cutoff 0.25
```

2. Check ligand RMSD:
```bash
echo "resname LIG" | gmx rms -s md.tpr -f md.xtc -o ligand_rmsd.xvg
```

3. Use more frames:
```bash
# Extract every frame instead of default stride
echo "resname LIG" | gmx trjconv -s md.tpr -f md.xtc -o ligand_full.xtc -dt 0
```

---

### ERROR-007: Hydrophobic contact analysis empty
**Symptom**: No hydrophobic contacts detected

**Cause**:
- No hydrophobic residues near ligand
- Cutoff too small
- Ligand not hydrophobic

**Fix**:
1. Increase cutoff:
```bash
binding-analysis hydrophobic -s md.tpr -f md.xtc --cutoff 0.6
```

2. Check nearby residues:
```bash
gmx select -s md.tpr -select "same residue as (within 0.8 of resname LIG)"
```

3. Visualize in VMD/PyMOL to confirm binding mode

---

### ERROR-008: Energy decomposition not detailed enough
**Symptom**: Only simplified contact analysis available

**Cause**: gmx_MMPBSA not installed or not configured

**Fix**:
1. Install gmx_MMPBSA:
```bash
pip install gmx_MMPBSA
```

2. Prepare topology files (requires AMBER format):
```bash
# Convert GROMACS topology to AMBER
# See gmx_MMPBSA documentation for details
```

3. Alternative: Use interaction energy from .edr:
```bash
echo "Coul-SR:Protein-LIG LJ-SR:Protein-LIG" | gmx energy -f md.edr -o interaction.xvg
```

---

### ERROR-009: MM-PBSA calculation too slow
**Symptom**: MM-PBSA takes hours or hangs

**Cause**:
- Too many frames
- Large system size
- PB solver slow

**Fix**:
1. Reduce number of frames:
```bash
binding-analysis mmpbsa -s md.tpr -f md.xtc --frames 50
```

2. Use GB instead of PB:
```bash
binding-analysis mmpbsa -s md.tpr -f md.xtc --method gb
```

3. Extract subset of trajectory:
```bash
echo "System" | gmx trjconv -s md.tpr -f md.xtc -o md_subset.xtc -b 5000 -e 10000 -dt 100
```

---

### ERROR-010: Interaction fingerprint incomplete
**Symptom**: Some analysis files missing (hbond_pl.xvg, mindist_pl.xvg, etc.)

**Cause**:
- Individual gmx commands failed silently
- Incorrect group names
- Trajectory format issues

**Fix**:
1. Run commands individually to see errors:
```bash
echo "Protein LIG" | gmx hbond -s md.tpr -f md.xtc -num hbond.xvg
echo "Protein LIG" | gmx mindist -s md.tpr -f md.xtc -od mindist.xvg
```

2. Check available groups:
```bash
gmx make_ndx -f md.tpr
# Type 'q' to quit and see group list
```

3. Create custom index file:
```bash
gmx make_ndx -f md.tpr -o index.ndx
# Select appropriate groups
binding-analysis interact -s md.tpr -f md.xtc -n index.ndx
```

---

## Performance Tips

### 1. Reduce trajectory size
```bash
# Extract every 10th frame
echo "System" | gmx trjconv -s md.tpr -f md.xtc -o md_stride.xtc -dt 10

# Use time window
binding-analysis mmpbsa -s md.tpr -f md.xtc -b 5000 -e 10000
```

### 2. Parallel analysis
```bash
# Run different analyses in parallel
binding-analysis hbond -s md.tpr -f md.xtc &
binding-analysis hydrophobic -s md.tpr -f md.xtc &
binding-analysis pocket -s md.tpr -f md.xtc &
wait
```

### 3. Use compressed trajectories
```bash
# GROMACS .xtc is already compressed
# Avoid converting to .trr unless needed
```

---

## Validation Checklist

Before running binding analysis, verify:

- [ ] Trajectory is equilibrated (check RMSD)
- [ ] Ligand remains bound (check mindist)
- [ ] System is properly centered and PBC-corrected
- [ ] Ligand residue name is known
- [ ] Sufficient sampling (> 10 ns recommended)
- [ ] Hydrogens present (for H-bond analysis)

---

## Quick Diagnostics

### Check ligand stability
```bash
echo "resname LIG" | gmx rms -s md.tpr -f md.xtc -o ligand_rmsd.xvg
# RMSD < 0.3 nm = stable binding
```

### Check protein-ligand distance
```bash
echo "Protein resname LIG" | gmx mindist -s md.tpr -f md.xtc -od mindist.xvg
# Distance < 0.5 nm = in contact
```

### Visualize binding mode
```bash
# Extract representative frame
echo "System" | gmx trjconv -s md.tpr -f md.xtc -o frame.pdb -dump 5000
# Open in VMD/PyMOL
```

---

## External Tools

### gmx_MMPBSA
- **Installation**: `pip install gmx_MMPBSA`
- **Documentation**: https://valdes-tresanco-ms.github.io/gmx_MMPBSA/
- **Use case**: Accurate binding free energy calculation

### ProLIF (Protein-Ligand Interaction Fingerprints)
- **Installation**: `pip install prolif`
- **Use case**: Detailed interaction fingerprinting
- **Python-based**: Requires trajectory conversion

### MDAnalysis
- **Installation**: `pip install MDAnalysis`
- **Use case**: Custom analysis scripts
- **Python-based**: Flexible but requires coding

---

## Contact and Support

For issues not covered here:
1. Check GROMACS manual: https://manual.gromacs.org/
2. GROMACS mailing list: gmx-users@gromacs.org
3. gmx_MMPBSA issues: https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/issues
