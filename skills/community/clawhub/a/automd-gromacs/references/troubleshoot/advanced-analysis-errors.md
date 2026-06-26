# advanced-analysis errors

## ERROR-001: covar failed

**Cause:** Selection group not found or trajectory issue

**Fix:**
```bash
# Check available groups
gmx make_ndx -f system.gro

# Use correct group
advanced-analysis -s md.tpr -f md.xtc --selection Backbone

# Common groups: C-alpha, Backbone, Protein, MainChain
```

**Auto-fix:** Script defaults to C-alpha if selection is empty

---

## ERROR-002: RMSD calculation failed

**Cause:** Trajectory or selection issue for clustering

**Fix:**
```bash
# Verify trajectory
gmx check -f md.xtc

# Test selection
echo "C-alpha" | gmx rms -s md.tpr -f md.xtc -o test.xvg

# Use simpler selection
advanced-analysis -s md.tpr -f md.xtc --type cluster --selection C-alpha
```

---

## ERROR-003: Ramachandran analysis failed

**Cause:** System does not contain protein or backbone atoms

**Fix:**
```bash
# Check if protein exists
gmx make_ndx -f md.tpr
# Look for "Protein" group

# Skip dihedral analysis for non-protein systems
advanced-analysis -s md.tpr -f md.xtc --type pca,cluster
```

---

## ERROR-004: Distance matrix calculation failed

**Cause:** Selection or trajectory issue for contact analysis

**Fix:**
```bash
# Use smaller selection
advanced-analysis -s md.tpr -f md.xtc --type contact --selection C-alpha

# Reduce time range
advanced-analysis -s md.tpr -f md.xtc --type contact -b 5000 -e 10000

# Skip frames
advanced-analysis -s md.tpr -f md.xtc --type contact --skip 10
```

---

## ERROR-005: Covariance calculation failed (DCCM)

**Cause:** Too many atoms or insufficient memory

**Fix:**
```bash
# Use C-alpha only
advanced-analysis -s md.tpr -f md.xtc --type dccm --dccm-selection C-alpha

# Reduce frames
gmx trjconv -f md.xtc -o reduced.xtc -skip 10
advanced-analysis -s md.tpr -f reduced.xtc --type dccm
```

---

## ERROR-006: PC projection failed (FEL)

**Cause:** PCA results not available or corrupted

**Fix:**
```bash
# Run PCA first
advanced-analysis -s md.tpr -f md.xtc --type pca

# Then run FEL
advanced-analysis -s md.tpr -f md.xtc --type fel

# Or run both together
advanced-analysis -s md.tpr -f md.xtc --type pca,fel
```

---

## WARNING: Cluster cutoff too small/large

**Cause:** CLUSTER_CUTOFF outside recommended range (0.05-0.5 nm)

**Auto-fix:** Script adjusts to 0.1-0.2 nm

**Manual override:**
```bash
# For tight clustering
advanced-analysis -s md.tpr -f md.xtc --type cluster --cluster-cutoff 0.08

# For loose clustering
advanced-analysis -s md.tpr -f md.xtc --type cluster --cluster-cutoff 0.25
```

---

## WARNING: Contact cutoff too small/large

**Cause:** CONTACT_CUTOFF outside recommended range (0.3-1.0 nm)

**Auto-fix:** Script adjusts to 0.4-0.6 nm

**Manual override:**
```bash
# For close contacts only
advanced-analysis -s md.tpr -f md.xtc --type contact --contact-cutoff 0.35

# For extended contacts
advanced-analysis -s md.tpr -f md.xtc --type contact --contact-cutoff 0.8
```

---

## Memory Issues

**Symptom:** Out of memory errors during analysis

**Fix:**
```bash
# 1. Use smaller selection
advanced-analysis -s md.tpr -f md.xtc --selection C-alpha

# 2. Reduce time range
advanced-analysis -s md.tpr -f md.xtc -b 5000 -e 10000

# 3. Skip frames
advanced-analysis -s md.tpr -f md.xtc --skip 10

# 4. Reduce trajectory size first
gmx trjconv -f md.xtc -o reduced.xtc -skip 5 -pbc mol -center
advanced-analysis -s md.tpr -f reduced.xtc
```

---

## PCA shows rotation instead of motion

**Cause:** Trajectory not fitted before PCA

**Fix:**
```bash
# Fit trajectory first
echo "Backbone Backbone" | gmx trjconv -s md.tpr -f md.xtc -o fitted.xtc -fit rot+trans

# Then run PCA
advanced-analysis -s md.tpr -f fitted.xtc --type pca
```

---

## Clustering produces too many/few clusters

**Cause:** Inappropriate cutoff for system dynamics

**Fix:**
```bash
# For more clusters (finer resolution)
advanced-analysis -s md.tpr -f md.xtc --type cluster --cluster-cutoff 0.1

# For fewer clusters (coarser grouping)
advanced-analysis -s md.tpr -f md.xtc --type cluster --cluster-cutoff 0.2

# Try different methods
advanced-analysis -s md.tpr -f md.xtc --type cluster --cluster-method linkage
```

---

## Ramachandran plot shows outliers

**Cause:** May indicate structural issues or flexible regions

**Interpretation:**
- Outliers in loops/turns are normal
- Outliers in helices/sheets may indicate problems
- Check if outliers are transient or persistent

**Fix:**
```bash
# Analyze specific residues
advanced-analysis -s md.tpr -f md.xtc --type dihedral --rama-residues 10-50

# Check RMSD for those regions
echo "10-50" | gmx rms -s md.tpr -f md.xtc -o rmsd_region.xvg
```

---

## Contact map shows unexpected patterns

**Cause:** PBC artifacts or improper preprocessing

**Fix:**
```bash
# Remove PBC first
gmx trjconv -s md.tpr -f md.xtc -o clean.xtc -pbc mol -center
# Select: Protein Protein

# Then analyze
advanced-analysis -s md.tpr -f clean.xtc --type contact
```

---

## DCCM shows weak correlations

**Cause:** Short simulation or highly flexible system

**Interpretation:**
- Weak correlations (<0.3) are common in flexible systems
- Need longer simulation for convergence
- Focus on strong correlations (>0.5)

**Fix:**
```bash
# Use longer trajectory
advanced-analysis -s md.tpr -f md.xtc --type dccm

# Or combine multiple trajectories
gmx trjcat -f traj1.xtc traj2.xtc traj3.xtc -o combined.xtc
advanced-analysis -s md.tpr -f combined.xtc --type dccm
```

---

## FEL shows flat landscape

**Cause:** Insufficient sampling or inappropriate PCs

**Fix:**
```bash
# Try different PC combinations
advanced-analysis -s md.tpr -f md.xtc --type fel --fel-pc1 1 --fel-pc2 3

# Increase bins for finer resolution
advanced-analysis -s md.tpr -f md.xtc --type fel --fel-bins 100

# Check if PC1-2 capture enough variance
# Should be >50% cumulative
```

---

## Performance Optimization

**For large systems:**
```bash
# 1. Use C-alpha only
advanced-analysis -s md.tpr -f md.xtc --selection C-alpha

# 2. Parallel processing
export OMP_NUM_THREADS=8
advanced-analysis -s md.tpr -f md.xtc

# 3. Skip frames
advanced-analysis -s md.tpr -f md.xtc --skip 5

# 4. Analyze specific time window
advanced-analysis -s md.tpr -f md.xtc -b 10000 -e 20000
```

---

## Interpretation Guidelines

### PCA
- **PC1 variance >30%:** Single dominant motion
- **PC1 variance <20%:** Multiple independent motions
- **Cumulative PC1-3 >60%:** Good representation
- **Sharp eigenvalue drop:** Few dominant modes

### Clustering
- **2-5 clusters:** Well-defined states
- **>10 clusters:** Highly dynamic system
- **1 cluster:** Stable conformation or poor sampling

### Ramachandran
- **>90% in favored regions:** Good structure
- **Outliers in loops:** Normal flexibility
- **Outliers in secondary structure:** Potential issues

### Contact Map
- **Persistent contacts (>80%):** Stable interactions
- **Transient contacts (20-50%):** Dynamic regions
- **Compare with crystal structure:** Validate simulation

### DCCM
- **Strong positive (>0.7):** Coupled motion
- **Strong negative (<-0.7):** Anti-correlated motion
- **Weak (<0.3):** Independent motion

### FEL
- **Single minimum:** Stable state
- **Multiple minima:** Conformational heterogeneity
- **High barriers (>10 kJ/mol):** Slow transitions
- **Low barriers (<5 kJ/mol):** Fast transitions

---

## Common Workflows

### Full analysis
```bash
advanced-analysis -s md.tpr -f md.xtc --type pca,cluster,dihedral,contact,dccm,fel
```

### Quick structural overview
```bash
advanced-analysis -s md.tpr -f md.xtc --type pca,cluster
```

### Detailed conformational analysis
```bash
advanced-analysis -s md.tpr -f md.xtc --type pca,fel --pca-extreme --fel-bins 100
```

### Protein-specific analysis
```bash
advanced-analysis -s md.tpr -f md.xtc --type dihedral,contact --selection Backbone
```

---

**Reference:** 
- GROMACS Manual Chapter 5.10 (Analysis)
- GROMACS Manual Chapter 8.7 (Covariance Analysis)
- Essential Dynamics: Amadei et al. (1993) Proteins 17:412
- GROMOS Clustering: Daura et al. (1999) Angew. Chem. Int. Ed. 38:236
