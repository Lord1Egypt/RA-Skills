# pca errors

## ERROR: covar failed

**Cause:** Group not found or trajectory issue

**Fix:**
```bash
# Check available groups
gmx make_ndx -f system.gro

# Use correct group
pca -s md.tpr -f md.xtc --group Backbone

# Common groups: C-alpha, Backbone, Protein
```

## ERROR: Not enough frames

**Cause:** Trajectory too short for meaningful PCA

**Fix:**
```bash
# Check frame count
gmx check -f md.xtc

# Need at least 100 frames for reliable PCA
# Reduce -dt or extend simulation
```

## ERROR: Memory allocation failed

**Cause:** Large system or many frames

**Fix:**
```bash
# Use smaller selection
pca -s md.tpr -f md.xtc --group C-alpha  # fewer atoms

# Or reduce frames
pca -s md.tpr -f md.xtc -b 5000 -e 10000  # shorter window

# Or skip frames
gmx trjconv -f md.xtc -o reduced.xtc -skip 10
pca -s md.tpr -f reduced.xtc
```

## WARNING: First PC explains <30% variance

**Cause:** Multiple independent motions

**Fix:**
```bash
# Analyze more PCs
pca -s md.tpr -f md.xtc --npc 20

# Check cumulative variance
head -30 pca_analysis/eigenval.xvg

# May need 5-10 PCs to capture 80% variance
```

## anaeig projection failed

**Cause:** Eigenvector file corrupted

**Fix:**
```bash
# Rerun covariance
cd pca_analysis
echo "C-alpha" | gmx covar -s ../md.tpr -f ../md.xtc -o eigenval.xvg -v eigenvec.trr

# Then project
echo "C-alpha" | gmx anaeig -s ../md.tpr -f ../md.xtc -v eigenvec.trr -first 1 -last 1 -proj proj_pc1.xvg
```

## Extreme structures look wrong

**Cause:** PBC not removed before PCA

**Fix:**
```bash
# Preprocess trajectory
gmx trjconv -s md.tpr -f md.xtc -o clean.xtc -pbc mol -center -fit rot+trans
# Select: Backbone Backbone

# Then run PCA
pca -s md.tpr -f clean.xtc --extreme
```

## PC1 shows rotation not motion

**Cause:** Trajectory not fitted

**Fix:**
```bash
# Fit trajectory first
echo "Backbone Backbone" | gmx trjconv -s md.tpr -f md.xtc -o fitted.xtc -fit rot+trans

# Then PCA
pca -s md.tpr -f fitted.xtc
```

## Interpretation tips

**PC1 captures largest motion:**
- Domain motion
- Loop flexibility
- Hinge bending

**Check eigenvalue distribution:**
```bash
# Plot eigenvalues
xmgrace pca_analysis/eigenval.xvg

# Sharp drop after PC1-3: few dominant motions
# Gradual decay: many small motions
```

**Visualize motion:**
```bash
# Generate movie along PC1
echo "C-alpha" | gmx anaeig -s md.tpr -f md.xtc -v eigenvec.trr -first 1 -last 1 -extr pc1_motion.pdb -nframes 20

# View in PyMOL
pymol pc1_motion.pdb
```

---

**Reference:** GROMACS Manual Ch. 8.7 (Covariance Analysis)
