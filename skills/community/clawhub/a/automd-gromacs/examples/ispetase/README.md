# ISPETase (PDB: 8H5K) — Complete MD Example

> Tested with GROMACS 2026.0 + AutoMD-GROMACS v5.0.0

## Protein

- **Name:** ISPETase (PET hydrolase)
- **PDB:** [8H5K](https://www.rcsb.org/structure/8H5K)
- **Organism:** *Ideonella sakaiensis*
- **Mutations:** N37D/S121E/R132E/A171C/A180V/P181V/D186H/S193C/R224E/N233C/S242T/N246D/S282C
- **Size:** 260 residues, ~29 kDa
- **Relevance:** Key enzyme for PET plastic biodegradation

## Results Summary

| Metric | Value | Status |
|--------|-------|--------|
| System size | 2,010 protein + 10,127 H₂O + 63 ions | 32,367 atoms |
| Box | Dodecahedron, 7.89 nm | ✅ |
| EM convergence | Fmax < 1000 kJ/mol/nm | ✅ |
| NVT (5 ps) | 300 K, stable | ✅ |
| NPT (5 ps) | Density 1025.4 kg/m³ | ✅ |
| Production (10 ps) | 20.5 ns/day (4-core CPU) | ✅ |
| RMSD (final) | 0.062 nm | Very stable |
| Rg (final) | 1.676 nm | Compact |

## Quick Reproduce

```bash
# 1. Download structure
wget https://files.rcsb.org/download/8H5K.pdb

# 2. Clean PDB (remove non-ATOM lines)
grep "^ATOM" 8H5K.pdb > protein_clean.pdb

# 3. System setup
bash scripts/basic/setup.sh \
    --input protein_clean.pdb \
    --output ./system \
    --forcefield amber99sb-ildn \
    --water tip3p \
    --box-type dodecahedron \
    --box-distance 1.2

# 4. Equilibration (5 ps NVT + 5 ps NPT)
cd system
NVT_STEPS=2500 NPT_STEPS=2500 \
    INPUT_GRO=em.gro INPUT_TOP=topol.top \
    bash ../../scripts/basic/equilibration.sh

# 5. Production (10 ps)
mkdir -p production && cd production
# Use prod.mdp from examples/ispetase/production/
gmx grompp -f prod.mdp -c ../equilibration/npt.gro \
    -r ../equilibration/npt.gro -t ../equilibration/npt.cpt \
    -p ../topol.top -o prod.tpr -maxwarn 1
gmx mdrun -v -deffnm prod -ntmpi 1 -ntomp 4

# 6. Basic analysis
cd ../ && mkdir analysis && cd analysis
printf "Backbone\nBackbone\n" | gmx rms -s ../production/prod.tpr -f ../production/prod.trr -o rmsd.xvg -fit rot+trans
printf "C-alpha\n" | gmx rmsf -s ../production/prod.tpr -f ../production/prod.trr -o rmsf.xvg -res
printf "Protein\n" | gmx gyrate -s ../production/prod.tpr -f ../production/prod.trr -o gyrate.xvg
```

## Input Files

- `input/8H5K.pdb` — Original PDB from RCSB
- `input/protein_clean.pdb` — ATOM-only filtered (2,010 atoms)

## Output Files

- `setup/topol.top` — Full topology (amber99sb-ildn + tip3p)
- `setup/REPORT.md` — System composition report
- `equilibration/npt.gro` — Equilibrated coordinates
- `equilibration/EQUILIBRATION_REPORT.md` — Equilibration diagnostics
- `production/prod.mdp` — Production run parameters (10 ps)
- `production/prod.log` — MD run log
- `analysis/rmsd.xvg` — Backbone RMSD (final: 0.062 nm)
- `analysis/rmsf.xvg` — C-α RMSF per residue
- `analysis/gyrate.xvg` — Radius of gyration (final: 1.676 nm)

## Advanced Analysis

```bash
# PCA: covariance matrix
printf "C-alpha\nC-alpha\n" | gmx covar -s ../production/prod.tpr -f ../production/prod.trr -o eigenval.xvg -v eigenvec.trr

# PCA: 2D projection
printf "C-alpha\nC-alpha\n" | gmx anaeig -s ../production/prod.tpr -f ../production/prod.trr -v eigenvec.trr -eig eigenval.xvg -2d proj2d.xvg -first 1 -last 2

# RMSD matrix + clustering
printf "Backbone\nBackbone\n" | gmx rms -s ../production/prod.tpr -f ../production/prod.trr -f2 ../production/prod.trr -m rmsd_matrix.xpm -fit rot+trans
printf "Backbone\nBackbone\n" | gmx cluster -s ../production/prod.tpr -f ../production/prod.trr -dm rmsd_matrix.xpm -o clusters.xpm -method gromos -cutoff 0.15
```

### Advanced Outputs
- `analysis_advanced/eigenval.xvg` — PCA eigenvalues
- `analysis_advanced/proj1.xvg` — PC1 projection
- `analysis_advanced/proj2d.xvg` — PC1 vs PC2 projection
- `analysis_advanced/clusters.xpm` — GROMOS clustering (cutoff 0.15 nm)
- `analysis_advanced/cluster.log` — Cluster statistics

## Extended Properties Analysis

```bash
# Run extended properties (dipole, potential, free volume, water ordering)
TRJ=../production/prod.trr TPR=../production/prod.tpr \
    bash ../../scripts/analysis/property-extended.sh
```

### Properties Results
| Property | Value |
|---|---|
| Dipole moment | ~640 Debye (fluctuating) |
| Dielectric constant | ε = 1.09 |
| Free volume fraction | 0.251 ± 0.001 |
| Molecular volume | 0.0335 ± 0.0002 nm³ |

### Property Outputs
- `analysis_properties/dipoles.xvg` — Total dipole moment vs time
- `analysis_properties/epsilon.xvg` — Dielectric constant estimate
- `analysis_properties/potential.xvg` — Electrostatic potential along Z-axis
- `analysis_properties/freevolume.xvg` — Molecular + vdW volumes
- `analysis_properties/h2order.xvg` — Water molecule orientation
- `analysis_properties/PROPERTIES_REPORT.md` — Summary report
