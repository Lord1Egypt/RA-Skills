# workflow errors

## ERROR: Input PDB not found

**Cause:** File path wrong

**Fix:**
```bash
# Check path
ls *.pdb

# Use absolute path
workflow -i /path/to/protein.pdb
```

## pdb2gmx failed: Unknown residue

**Cause:** Non-standard residues or ligands

**Fix:**
```bash
# Clean PDB first
grep "^ATOM" protein.pdb | grep -v "HOH\|HET" > clean.pdb

# Or use different force field
workflow -i protein.pdb --ff charmm36
```

## EM not converging

**Cause:** Bad initial structure

**Fix:**
```bash
# Check EM log
tail -50 workflow_output/em/em.log

# If LINCS warnings, structure has clashes
# Fix PDB or increase emtol in script
```

## NVT temperature unstable

**Cause:** System not equilibrated

**Fix:**
```bash
# Extend NVT
cd workflow_output/nvt
gmx mdrun -v -deffnm nvt -cpi nvt.cpt -nsteps 100000  # double time

# Check temperature
echo "Temperature" | gmx energy -f nvt.edr -o temp.xvg
```

## NPT pressure fluctuating

**Cause:** Normal for small systems

**Fix:**
```bash
# Check if density stabilizes
echo "Density" | gmx energy -f npt.edr -o density.xvg

# If stable, pressure fluctuations OK
# For large fluctuations, extend NPT
```

## MD crashes early

**Cause:** Insufficient equilibration

**Fix:**
```bash
# Extend equilibration
cd workflow_output/npt
gmx mdrun -v -deffnm npt -cpi npt.cpt -nsteps 100000

# Then restart MD
cd ../md
gmx grompp -f md.mdp -c ../npt/npt.gro -t ../npt/npt.cpt -p ../setup/topol.top -o md.tpr
gmx mdrun -v -deffnm md
```

## Out of disk space

**Cause:** Long MD generates large files

**Fix:**
```bash
# Check space
df -h

# Reduce output frequency in md.mdp
nstxout-compressed = 10000  # save every 20 ps instead of 10 ps

# Or compress trajectory
gmx trjconv -f md.xtc -o md_compressed.xtc -skip 2
```

## Workflow interrupted

**Cause:** System crash or manual stop

**Fix:**
```bash
# Resume from last checkpoint
cd workflow_output/md
gmx mdrun -v -deffnm md -cpi md.cpt

# Or restart from last phase
# Check which phase completed:
ls -lh */
```

## Customization tips

**Change simulation time:**
```bash
workflow -i protein.pdb --mdtime 50  # 50 ns
```

**Different force field:**
```bash
workflow -i protein.pdb --ff charmm36-jul2022
```

**Larger box:**
```bash
workflow -i protein.pdb --box 1.5  # 1.5 nm margin
```

**Skip analysis (faster):**
```bash
workflow -i protein.pdb --quick
```

**Modify MDP parameters:**
```bash
# Edit script or manually edit MDP files
# in workflow_output/*/
```

---

**Reference:** GROMACS Manual Ch. 3 (Getting Started)
