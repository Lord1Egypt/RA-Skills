---
name: amber-mmgbsa
description: |
  End-to-end guide for running MM/GBSA binding free energy calculations using AmberTools/Amber
  on a pre-existing receptor–ligand complex without molecular dynamics sampling. Covers
  structure preparation, GAFF2 ligand parameterisation, topology construction, single-frame
  trajectory generation, MMPBSA.py execution, and result interpretation with explicit
  uncertainty boundaries. Suitable for crystal-pose scoring, post-docking rapid screening,
  and mechanistic energy decomposition.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧪",
        "examples":
          [
            "run MM/GBSA on a receptor and ligand without MD sampling",
            "single-structure MMPBSA.py workflow for a crystal complex",
            "how to calculate binding energy from receptor.pdb and ligand.pdb with Amber",
            "Amber MM/GBSA tutorial no dynamics"
          ]
      }
  }
---

# Amber MM/GBSA — Single-Structure Workflow

## Overview

This skill describes a complete, production-ready workflow for computing
**MM/GBSA (Molecular Mechanics / Generalized Born Surface Area) binding free
energies** using **AmberTools / Amber** on a **single static structure** — no
molecular dynamics sampling required.

It is designed for two primary use cases:

1. **Rapid pose scoring** — evaluate the binding energy of a crystal
   structure or a top docking pose without running an MD simulation.
2. **Mechanistic decomposition** — obtain a standard breakdown
   `VDWAALS / EEL / EGB / ESURF / ΔG_bind` to interpret which interactions
   drive or oppose binding.

> **Scope note:** This workflow computes a single-structure enthalpy-like
> MM/GBSA estimate. It does not include conformational entropy, water-mediated
> interactions, or ensemble averaging. For quantitative ranking of multiple
> ligands or for results intended to compare with experimental ΔG values,
> a full MD trajectory + MMPBSA.py ensemble average is strongly recommended.

---

## Prerequisites

### Software

| Tool | Version | Purpose |
|------|---------|---------|
| `tleap` | AmberTools 20+ | System building & topology |
| `antechamber` | AmberTools 20+ | Ligand parameterisation |
| `parmchk2` | AmberTools 20+ | Missing GAFF2 parameters |
| `cpptraj` | AmberTools 20+ | Trajectory extraction |
| `MMPBSA.py` | AmberTools 20+ | MM/GBSA calculation |
| `parmed` | any recent | Topology inspection & merging |

Set your environment:

```bash
export AMBERHOME=/path/to/amber24   # adjust to your installation
export PATH=$AMBERHOME/bin:$PATH
PY=$AMBERHOME/miniconda/bin/python  # preferred Python
```

### Input files required

| File | Description |
|------|-------------|
| `receptor.pdb` | Receptor (protein ± DNA ± metals) with correct residue names |
| `ligand.pdb` | Ligand with 3D coordinates, correct bond orders, and known net charge |

---

## Recommended Directory Layout

```text
project_mmgbsa/
├── input/
│   ├── receptor.pdb
│   └── ligand.pdb
├── prep/          # cleaned structures
├── build/         # topologies and coordinates
├── traj/          # single-frame trajectories
├── mmgbsa/        # MMPBSA.py inputs and outputs
└── logs/          # all log files
```

---

## Step-by-Step Protocol

### Step 0 — Verify Input Structures

Before any calculation, confirm:

- **Receptor:** Standard Amber residue names (protein: standard 20 aa; DNA: DC/DA/DG/DT; water: WAT/HOH). Remove缓冲 salts and small molecules with no parameters.
- **Ligand:** 3D coordinates present; bond orders chemically reasonable; net charge known.
- **Complex geometry:** Receptor and ligand must already be in the correct binding pose (crystal structure or top-ranked docking pose). They cannot be randomly docked in separate files without a reference complex.

---

### Step 1 — Clean the Receptor PDB

Rename crystallographic water to Amber-compatible WAT:

```bash
mkdir -p prep logs
awk '
BEGIN{OFS=""}
/^ATOM|^HETATM/ {
  res=substr($0,18,3)
  if (res=="HOH") {
    print substr($0,1,17),"WAT",substr($0,21)
  } else {
    print $0
  }
  next
}
{print}
' input/receptor.pdb > prep/receptor_clean.pdb
```

> **Should I keep crystallographic waters?** Usually remove them for MM/GBSA unless a specific water is structurally validated as a key bridging molecule. If retained, document this decision and apply it consistently across all compared systems.

---

### Step 2 — Parameterise the Ligand (GAFF2)

#### 2a. Generate GAFF2 mol2 with AM1-BCC charges

```bash
cd prep
antechamber \
  -i ../input/ligand.pdb \
  -fi pdb \
  -o ligand.mol2 \
  -fo mol2 \
  -c bcc \
  -nc 0 \
  -at gaff2 \
  -j 4 \
  > ../logs/antechamber.log 2>&1

# Verify mol2 was produced
ls -lh ligand.mol2
```

**Critical:** The `-nc` value must match the true formal charge of the ligand.
Common examples:
- Neutral organic molecule → `-nc 0`
- Carboxylate → `-nc -1`
- Phosphate → `-nc -2` or `-3`
- Metal complex → confirm charge separately

#### 2b. Check for missing force-field parameters

```bash
parmchk2 \
  -i ligand.mol2 \
  -f mol2 \
  -o ligand.frcmod \
  > ../logs/parmchk2.log 2>&1

# If "frcmod" is empty or missing params are critical, either:
#   a) re-draw the problematic substructure in the PDB
#   b) manually add parameters to the frcmod file
```

---

### Step 3 — Build the Receptor Topology

#### Protein only

```bash
mkdir -p build
cat > build/tleap_rec.in <<'EOF'
source leaprc.protein.ff14SB
source leaprc.water.tip3p

rec = loadpdb ../prep/receptor_clean.pdb
desc rec
saveamberparm rec receptor.prmtop receptor.inpcrd
quit
EOF

tleap -f build/tleap_rec.in > logs/tleap_rec.log 2>&1
```

#### Protein + DNA

```bash
cat > build/tleap_rec.in <<'EOF'
source leaprc.protein.ff14SB
source leaprc.DNA.OL15
source leaprc.water.tip3p

rec = loadpdb ../prep/receptor_clean.pdb
desc rec
saveamberparm rec receptor.prmtop receptor.inpcrd
quit
EOF

tleap -f build/tleap_rec.in > logs/tleap_rec.log 2>&1
```

#### Protein + DNA + metal ions or special groups

```bash
cat > build/tleap_rec.in <<'EOF'
source leaprc.protein.ff14SB
source leaprc.DNA.OL15
loadoff $AMBERHOME/dat/leap/lib/terminal_monophosphate.lib
source leaprc.water.tip3p

rec = loadpdb ../prep/receptor_clean.pdb
desc rec
saveamberparm rec receptor.prmtop receptor.inpcrd
quit
EOF

tleap -f build/tleap_rec.in > logs/tleap_rec.log 2>&1
```

**Verify success:**

```bash
ls -lh build/receptor.prmtop build/receptor.inpcrd
# receptor.prmtop should be > 10 KB for a realistic protein
```

---

### Step 4 — Build the Ligand Topology

```bash
cat > build/tleap_lig.in <<'EOF'
source leaprc.gaff2
lig = loadmol2 ../prep/ligand.mol2
loadAmberParams ../prep/ligand.frcmod
desc lig
saveamberparm lig ligand.prmtop ligand.inpcrd
quit
EOF

tleap -f build/tleap_lig.in > logs/tleap_lig.log 2>&1

# Verify and inspect charge
$PY -c "import parmed as p; r=p.load_file('build/ligand.prmtop'); print(f'Ligand charge: {r.charge:.4f}')"
```

---

### Step 5 — Build the Complex Topology (Consistent Atom Types)

The key rule: **receptor and ligand topologies must come from the same tleap session** to ensure atom type definitions are mutually consistent.

```bash
cat > build/tleap_complex.in <<'EOF'
source leaprc.protein.ff14SB
source leaprc.DNA.OL15
source leaprc.gaff2
source leaprc.water.tip3p

lig = loadmol2 ../prep/ligand.mol2
loadAmberParams ../prep/ligand.frcmod

rec = loadpdb ../prep/receptor_clean.pdb

desc rec
desc lig

# Save all three topologies from the same session
saveamberparm rec receptor_final.prmtop receptor_final.inpcrd
saveamberparm lig ligand_final.prmtop ligand_final.inpcrd
quit
EOF

tleap -f build/tleap_complex.in > logs/tleap_complex.log 2>&1

ls -lh build/receptor_final.prmtop build/ligand_final.prmtop
```

**Optional — ParmEd merge** (if you need a single complex topology):

```python
# build/merge_complex.py
import parmed as p, os

rec = p.load_file('build/receptor_final.prmtop', 'build/receptor_final.inpcrd')
lig = p.load_file('build/ligand_final.prmtop', 'build/ligand_final.inpcrd')

complex_sys = rec + lig
complex_sys.save('build/complex.prmtop', overwrite=True)
complex_sys.save('build/complex.inpcrd', overwrite=True)

print(f"Receptor:   {rec.atoms} atoms,  charge={rec.charge:.4f}")
print(f"Ligand:     {lig.atoms} atoms,  charge={lig.charge:.4f}")
print(f"Complex:    {complex_sys.atoms} atoms, charge={complex_sys.charge:.4f}")
```

---

### Step 6 — Generate Single-Frame NetCDF Trajectories

`MMPBSA.py` requires trajectory inputs. For a single-structure calculation, convert the `inpcrd` restart file into a **single-frame NetCDF**:

```bash
mkdir -p traj logs

# Receptor
cpptraj <<'EOF' > logs/cpptraj_rec.log 2>&1
parm ../build/receptor.prmtop
trajin ../build/receptor.inpcrd
trajout receptor_traj.nc netcdf
run
EOF

# Ligand
cpptraj <<'EOF' > logs/cpptraj_lig.log 2>&1
parm ../build/ligand.prmtop
trajin ../build/ligand.inpcrd
trajout ligand_traj.nc netcdf
run
EOF

# Complex
cpptraj <<'EOF' > logs/cpptraj_com.log 2>&1
parm ../build/complex.prmtop
trajin ../build/complex.inpcrd
trajout complex_traj.nc netcdf
run
EOF

ls -lh traj/*.nc
```

> If the ligand and receptor topologies share a consistent type table (from Step 5), they can also share a single `complex_traj.nc` in **single-trajectory mode**.

---

### Step 7 — Write MMPBSA.py Input Files

#### 7a. Standard MM/GBSA (total energy only)

Save as `mmgbsa/mmpbsa.in`:

```bash
&general
  startframe=1,
  endframe=1,
  interval=1,
  verbose=1,
  keep_files=0,
/
&gb
  igb=5,
  saltcon=0.150,
  surften=0.005,
  surfoff=0.000,
  molsurf=0,
  radiopt=1,
/
```

#### 7b. MM/GBSA with per-residue decomposition

Save as `mmgbsa/mmpbsa_decomp.in`:

```bash
&general
  startframe=1,
  endframe=1,
  interval=1,
  verbose=1,
  keep_files=0,
/
&gb
  igb=5,
  saltcon=0.150,
  surften=0.005,
  surfoff=0.000,
  molsurf=0,
  radiopt=1,
/
&decomp
  idecomp=1,
  dec_verbose=0,
  print_res="within 6",
/
```

**Key parameter reference:**

| Parameter | Recommended value | Notes |
|-----------|------------------|-------|
| `igb` | `5` | GB-neck2 (recommended for proteins) |
| `saltcon` | `0.150` | physiological ionic strength (M) |
| `surften` | `0.005` | standard surface tension term |
| `molsurf` | `0` | use LCPO surface area |
| `radiopt` | `1` | radii from prmtop (matching force field) |
| `print_res` | `"within 6"` | only residues within 6 Å of ligand |

---

### Step 8 — Run MMPBSA.py

```bash
mkdir -p mmgbsa logs

MMPBSA.py \
  -O \
  -i mmgbsa/mmpbsa.in \
  -cp build/complex.prmtop \
  -rp build/receptor.prmtop \
  -lp build/ligand.prmtop \
  -y traj/complex_traj.nc \
  -o mmgbsa/FINAL_RESULTS_MMPBSA.dat \
  > logs/mmpbsa.log 2>&1
```

With decomposition:

```bash
MMPBSA.py \
  -O \
  -i mmgbsa/mmpbsa_decomp.in \
  -cp build/complex.prmtop \
  -rp build/receptor.prmtop \
  -lp build/ligand.prmtop \
  -y traj/complex_traj.nc \
  -o mmgbsa/FINAL_RESULTS_MMPBSA.dat \
  -do mmgbsa/FINAL_DECOMP_MMPBSA.dat \
  > logs/mmpbsa_decomp.log 2>&1
```

---

## Interpreting the Results

### Standard Energy Terms

| Term | Physical meaning | Sign convention |
|------|-----------------|-----------------|
| `VDWAALS` | van der Waals / hydrophobic interactions | **Negative = favorable** |
| `EEL` | Gas-phase electrostatic energy | Negative usually favorable; large positive often indicates charge–charge repulsion |
| `EGB` | Polar solvation free energy (GB) | **Negative = favorable** (desolvation gain) |
| `ESURF` | Nonpolar solvation (surface area term) | **Negative = favorable** |
| `ΔG_bind` | Net binding free energy | **Negative = favorable** |

The net binding energy is:

```
ΔG_bind = VDWAALS + EEL + EGB + ESURF
```

---

### When Large Cancellation Occurs

In systems with **highly charged components** (e.g., DNA-binding proteins, phosphate-containing ligands, multi-metal active sites), you may observe:

```
EEL  = +700   (large unfavorable)
EGB  = −660   (large favorable, compensating)
ΔG_bind ≈ −0.7  (small net, from large cancellation)
```

**This pattern is arithmetically valid but physically fragile.** The final `ΔG_bind` value in such cases is extremely sensitive to:

- Small errors in atomic charges
- Conformational sampling
- The GB solvent model approximation
- Whether metals/waters are included

**Correct interpretation:** Report that the net binding is weakly favorable or inconclusive, and note that electrostatic terms largely cancel. Do **not** treat a near-zero `ΔG_bind` from large cancellation as evidence of "no binding" or as a precise quantitative affinity.

---

### Recommended Results Table for Reports

Present results as:

| Energy Component | Value (kcal/mol) | Interpretation |
|-----------------|-----------------|----------------|
| VDWAALS | −36.99 | Favorable: hydrophobic / shape complementarity |
| EEL | +702.60 | Unfavorable: charge–charge repulsion (both partners negatively charged) |
| EGB | −662.23 | Favorable: polar desolvation gain upon binding |
| ESURF | −4.14 | Favorable: nonpolar surface burial |
| **ΔG_bind** | **−0.76** | Net weakly favorable; dominated by electrostatic cancellation |

Follow with a method note:

> *"ΔG_bind was calculated using the MM/GBSA method (igb=5, saltcon=0.15 M) on a single crystal/pose structure without conformational sampling or entropy correction. Absolute values are estimates and should not be directly compared to experimental binding free energies without further validation."*

---

## Common Errors and Troubleshooting

### Error 1 — `Unknown residue` in tleap log

**Cause:** Non-standard residue name in PDB.  
**Fix:** Remap to Amber-compatible names using `pdb4amber` or manually edit the PDB.

### Error 2 — `antechamber` fails to produce mol2

**Cause:** Malformed PDB (missing bonds), wrong net charge, or unsupported elements.  
**Fix:**
```bash
# Check and fix the PDB
babel -ipdb ligand.pdb -osmi   # view SMILES
# Re-draw or re-fetch the ligand structure
```

### Error 3 — Atom count mismatch between topologies and trajectories

**Cause:** Running `tleap` separately for receptor and ligand without a shared session.  
**Fix:** Rebuild both from a single `tleap_complex.in` (Step 5).

### Error 4 — Extreme EEL / EGB values (hundreds of kcal/mol)

**Cause:** System contains exposed charged groups, metals, or phosphate groups; GB model amplifies the gas-phase/solvation contrast.  
**Fix:** Confirm this is expected for your system. Do not round/force these values. Report them honestly and flag the result as "large-cancellation regime."

### Error 5 — `MMPBSA.py` crashes with `Segmentation fault`

**Cause:** Usually insufficient memory or a mismatch between trajectory frame count and topology.  
**Fix:**
```bash
# Check trajectory frame count
cpptraj -p build/complex.prmtop -y traj/complex_traj.nc -e 1 <<'EOF'
EOF
# Set startframe/endframe explicitly in mmpbsa.in
```

---

## Minimum Deliverables for a Publication-Ready Result

When presenting MM/GBSA results in a paper or report, include:

1. **Energy table** — all terms with units (kcal/mol)
2. **Method paragraph** — force field, GB model, radii set, salt concentration, single vs. multi-frame
3. **System description** — protein + DNA ± metals ± waters, net charges, ligand type
4. **Explicit limitation statement** — single structure, no entropy correction, GB model limitations
5. **Source data** — enough to reproduce: input PDBs, topologies, mmpbsa.in, and raw output log

---

## Quick-Reference Command Summary

```bash
# 1. Ligand parameterisation
antechamber -i ligand.pdb -fi pdb -o ligand.mol2 -fo mol2 -c bcc -nc CHARGE -at gaff2 -j 4
parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod

# 2. Receptor topology
tleap -f tleap_rec.in

# 3. Ligand topology
tleap -f tleap_lig.in

# 4. Single-frame trajectories
cpptraj -p complex.prmtop -y complex.inpcrd -o complex_traj.nc netcdf

# 5. MM/GBSA
MMPBSA.py -i mmpbsa.in -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop -y complex_traj.nc -o FINAL_RESULTS.dat
```

---

## When to Upgrade to MD-Based MM/GBSA

If your single-structure result is close to zero, involves large electrostatic cancellation, or will be used to **rank multiple ligands**, upgrade to the full MD-based workflow:

- Run at least **100 ns** of production MD per system
- Extract **100–200 snapshots** (every 0.5–1 ns)
- Use **three-trajectory mode** (complex / receptor / ligand trajectories)
- Compute **block averages** to estimate statistical uncertainty
- Add **normal mode analysis** or **quasi-harmonic entropy** if feasible
- Run **at least 2–3 independent replicates** per system

---

## One-Sentence Takeaway

**Amber single-structure MM/GBSA is a fast, interpretable binding energy estimator; when electrostatic terms dominate and cancel, treat the absolute ΔG_bind as a directional indicator rather than a quantitative affinity — and always upgrade to MD ensemble sampling for comparative rankings.**
