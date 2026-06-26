---
name: amber-md
description: |
  Official-style Amber24 molecular dynamics workflow guide for proteins. Includes a standard end-to-end Amber MD procedure, command templates, input-file templates, and a complete manual worked example from PDB download through RMSD/RMSF analysis. This is a documentation-oriented scientific skill for reproducible research workflows in Amber.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧬",
        "examples":
          [
            "how do I run Amber MD on a protein?",
            "show me a standard Amber workflow with commands",
            "give me a complete manual example for Amber RMSD and RMSF analysis"
          ]
      }
  }
---

# Amber Molecular Dynamics Simulation

## Overview

This skill is designed as an **official-style documentation page** for running a standard protein molecular dynamics workflow with **Amber24 / AmberTools24**.

It is intentionally **documentation-first**:
- it explains the canonical workflow,
- provides reusable command templates,
- provides input-file templates,
- and gives a full manual example that users can reproduce step by step.

It does **not** bundle executable automation scripts inside the public ClawHub package.

---

## What this skill helps you do

Use this skill when you need to:

1. prepare a protein structure from the PDB database,
2. build a solvated Amber system,
3. run minimization, heating, equilibration, and production MD,
4. analyze the trajectory with `cpptraj`,
5. understand what outputs to expect and how to judge simulation quality.

---

## Recommended Amber tools

| Tool | Main purpose |
|---|---|
| `pdb4amber` | preprocess PDB structures for Amber |
| `tleap` | build topology and coordinates |
| `pmemd.cuda` | GPU production MD |
| `pmemd` | CPU fallback |
| `cpptraj` | trajectory analysis |
| `antechamber` | ligand parameterization when needed |
| `parmchk2` | missing force-field terms for ligands |

---

## Standard workflow summary

| Stage | Goal | Main output |
|---|---|---|
| 1. Structure preparation | clean and standardize input structure | processed PDB |
| 2. System building | add force field, solvent, ions | `prmtop`, `inpcrd` |
| 3. Minimization | remove bad contacts | minimized restart file |
| 4. NVT heating | raise temperature to target value | heated restart + trajectory |
| 5. NPT equilibration | stabilize density and pressure | equilibrated restart + trajectory |
| 6. Production MD | generate scientific trajectory | production trajectory |
| 7. Analysis | compute RMSD/RMSF and related metrics | data tables and plots |

---

## Recommended directory layout

```text
project/
├── input/
│   └── protein.pdb
├── build/
├── md/
├── analysis/
└── logs/
```

A simpler flat directory also works, but a structured layout improves reproducibility.

---

## 1. Structure preparation

### Recommended rules

- If the PDB entry contains multiple NMR models, start with **Model 1**.
- Remove unsupported ligands if you do not have parameters for them.
- Keep the protein-only workflow as the default baseline.
- Use `pdb4amber` to standardize residue names and protonation-related formatting.

### Command template

```bash
mkdir -p input build md analysis logs
cd project

# download from RCSB
wget -O input/1AKI.pdb https://files.rcsb.org/download/1AKI.pdb

# preprocess
pdb4amber -i input/1AKI.pdb -o input/1AKI_amber.pdb --reduce > logs/pdb4amber.log 2>&1
```

### Notes

- If preprocessing fails because of nonstandard residues, inspect the structure first.
- For protein-only tutorials, removing unsupported ligands is often the most robust starting point.

---

## 2. System building with tleap

### Recommended setup

- Protein force field: `ff19SB`
- Water model: `OPC`
- Box type: truncated octahedron
- Padding: ~15 Å
- Neutralization: `Na+` / `Cl-`

### `tleap` input template

Save as `build/tleap.in`:

```bash
source leaprc.protein.ff19SB
source leaprc.water.opc

mol = loadPDB ../input/1AKI_amber.pdb

desc mol
addions mol Cl- 0
addions mol Na+ 0
solvateOct mol OPCBOX 15.0
addions2 mol Na+ 0
addions2 mol Cl- 0

saveAmberParm mol prmtop inpcrd
savePDB mol solvated.pdb
quit
```

### Run command

```bash
cd build
tleap -f tleap.in > ../logs/tleap.log 2>&1
```

### Expected outputs

- `build/prmtop`
- `build/inpcrd`
- `build/solvated.pdb`

---

## 3. Energy minimization

A common two-stage minimization is sufficient for many small-to-medium protein systems.

### Stage 1 minimization template

Save as `md/min1.in`:

```bash
Stage 1 minimization
 &cntrl
  imin=1,
  maxcyc=5000,
  ncyc=2500,
  ntb=1,
  ntr=0,
  cut=10.0,
  ntpr=500,
 /
```

Run:

```bash
cd md
pmemd.cuda -O \
  -i min1.in \
  -o min1.out \
  -p ../build/prmtop \
  -c ../build/inpcrd \
  -r min1.rst7
```

### Stage 2 minimization template

Save as `md/min2.in`:

```bash
Stage 2 minimization
 &cntrl
  imin=1,
  maxcyc=10000,
  ncyc=5000,
  ntb=1,
  ntr=0,
  cut=10.0,
  ntpr=1000,
 /
```

Run:

```bash
pmemd.cuda -O \
  -i min2.in \
  -o min2.out \
  -p ../build/prmtop \
  -c min1.rst7 \
  -r min2.rst7
```

---

## 4. NVT heating

### Heating template

Save as `md/heat.in`:

```bash
NVT heating
 &cntrl
  imin=0,
  irest=0,
  ntx=1,
  nstlim=50000,
  dt=0.002,
  ntf=2,
  ntc=2,
  tempi=0.0,
  temp0=300.0,
  ntt=3,
  gamma_ln=1.0,
  ntb=1,
  cut=10.0,
  ntpr=5000,
  ntwx=5000,
 /
```

Run:

```bash
pmemd.cuda -O \
  -i heat.in \
  -o heat.out \
  -p ../build/prmtop \
  -c min2.rst7 \
  -r heat.rst7 \
  -x heat.nc
```

---

## 5. NPT equilibration

### Equilibration template

Save as `md/equil.in`:

```bash
NPT equilibration
 &cntrl
  imin=0,
  irest=1,
  ntx=5,
  nstlim=100000,
  dt=0.002,
  ntf=2,
  ntc=2,
  temp0=300.0,
  ntt=3,
  gamma_ln=1.0,
  ntb=2,
  ntp=1,
  pres0=1.0,
  cut=10.0,
  ntpr=10000,
  ntwx=10000,
 /
```

Run:

```bash
pmemd.cuda -O \
  -i equil.in \
  -o equil.out \
  -p ../build/prmtop \
  -c heat.rst7 \
  -r equil.rst7 \
  -x equil.nc
```

---

## 6. Production MD

### 1 ns production template

Save as `md/prod.in`:

```bash
Production MD
 &cntrl
  imin=0,
  irest=1,
  ntx=5,
  nstlim=500000,
  dt=0.002,
  ntf=2,
  ntc=2,
  temp0=300.0,
  ntt=3,
  gamma_ln=1.0,
  ntb=2,
  ntp=1,
  pres0=1.0,
  cut=10.0,
  iwrap=1,
  ntpr=25000,
  ntwx=12500,
 /
```

Run:

```bash
pmemd.cuda -O \
  -i prod.in \
  -o prod.out \
  -p ../build/prmtop \
  -c equil.rst7 \
  -r prod.rst7 \
  -x prod.nc
```

### Useful duration reference

| Target time | `nstlim` with `dt=0.002 ps` |
|---|---|
| 1 ns | 500000 |
| 10 ns | 5000000 |
| 100 ns | 50000000 |

---

## 7. Trajectory analysis with cpptraj

### Recommended analysis procedure

Before RMSD/RMSF:
- strip solvent and ions if you want protein-only metrics,
- apply `autoimage`,
- use a consistent atom mask.

### `cpptraj` template

Save as `analysis/analyze.cpptraj`:

```bash
parm ../build/prmtop
trajin ../md/prod.nc 1 last 1

strip :WAT
strip :Na+
strip :Cl-
autoimage

rms out rmsd_ca.dat
atomicfluct out rmsf_ca.dat
run
```

Run:

```bash
cd analysis
cpptraj -i analyze.cpptraj > ../logs/cpptraj.log 2>&1
```

### Typical outputs

- `analysis/rmsd_ca.dat`
- `analysis/rmsf_ca.dat`
- `logs/cpptraj.log`

---

## Full manual example: protein-only 1 ns Amber MD

This example shows a minimal, reproducible manual workflow using **1AKI**.

### Step 1 — create directories

```bash
mkdir -p amber_1aki/{input,build,md,analysis,logs}
cd amber_1aki
```

### Step 2 — download and preprocess structure

```bash
wget -O input/1AKI.pdb https://files.rcsb.org/download/1AKI.pdb
pdb4amber -i input/1AKI.pdb -o input/1AKI_amber.pdb --reduce > logs/pdb4amber.log 2>&1
```

### Step 3 — create `build/tleap.in`

```bash
cat > build/tleap.in << 'EOF'
source leaprc.protein.ff19SB
source leaprc.water.opc
mol = loadPDB ../input/1AKI_amber.pdb
addions mol Cl- 0
addions mol Na+ 0
solvateOct mol OPCBOX 15.0
addions2 mol Na+ 0
addions2 mol Cl- 0
saveAmberParm mol prmtop inpcrd
savePDB mol solvated.pdb
quit
EOF
```

Run:

```bash
cd build
tleap -f tleap.in > ../logs/tleap.log 2>&1
cd ..
```

### Step 4 — create minimization, heating, equilibration, and production input files

Use the exact templates from the sections above:
- `md/min1.in`
- `md/min2.in`
- `md/heat.in`
- `md/equil.in`
- `md/prod.in`

### Step 5 — run MD

```bash
cd md
pmemd.cuda -O -i min1.in  -o min1.out  -p ../build/prmtop -c ../build/inpcrd -r min1.rst7
pmemd.cuda -O -i min2.in  -o min2.out  -p ../build/prmtop -c min1.rst7       -r min2.rst7
pmemd.cuda -O -i heat.in  -o heat.out  -p ../build/prmtop -c min2.rst7       -r heat.rst7  -x heat.nc
pmemd.cuda -O -i equil.in -o equil.out -p ../build/prmtop -c heat.rst7       -r equil.rst7 -x equil.nc
pmemd.cuda -O -i prod.in  -o prod.out  -p ../build/prmtop -c equil.rst7      -r prod.rst7  -x prod.nc
cd ..
```

### Step 6 — analyze trajectory

```bash
cat > analysis/analyze.cpptraj << 'EOF'
parm ../build/prmtop
trajin ../md/prod.nc 1 last 1
strip :WAT
strip :Na+
strip :Cl-
autoimage
rms out rmsd_ca.dat
atomicfluct out rmsf_ca.dat
run
EOF

cd analysis
cpptraj -i analyze.cpptraj > ../logs/cpptraj.log 2>&1
cd ..
```

### Step 7 — inspect results

```bash
ls -lh md/prod.nc analysis/rmsd_ca.dat analysis/rmsf_ca.dat
```

Expected scientific interpretation:
- RMSD reaches a stable plateau after equilibration,
- RMSF is higher at loops and termini,
- temperature remains close to 300 K,
- pressure fluctuates around 1 atm during NPT stages.

---

## Common quality checks

| Check | What to look for |
|---|---|
| Minimization | energy decreases and no severe bad contacts remain |
| Heating | temperature ramps smoothly toward 300 K |
| Equilibration | density/pressure behavior stabilizes |
| Production RMSD | plateau rather than monotonic drift |
| RMSF | flexible regions match structural expectation |

---

## Common pitfalls

1. **Using all atoms including water for RMSD**
   - this often produces meaningless large RMSD values.

2. **Ignoring ligands with missing parameters**
   - remove them or parameterize them first.

3. **Using inconsistent atom masks**
   - reference and trajectory selections must match.

4. **Skipping `autoimage`**
   - periodic boundary effects can distort analysis.

5. **Starting with too large a target simulation**
   - validate the workflow with 1 ns before 100 ns.

---

## Ligands and nonstandard residues

If your structure contains:
- a ligand,
- a cofactor,
- a metal center,
- a nucleotide analog,
- or another nonstandard residue,

then you may need:
- `antechamber`,
- `parmchk2`,
- additional `tleap` libraries,
- or specialized workflows such as `MCPB.py`.

For a first-pass reproducible workflow, a **protein-only simulation** is often the most robust baseline.

---

## References included in this skill

- `references/amber_parameter_guide.md`
- `references/cpptraj_analysis_guide.md`

---

## Intended use

This public ClawHub version is intended for:
- scientific education,
- workflow standardization,
- project planning,
- manual reproducible Amber execution.

It is a **public documentation edition** rather than a bundled executable automation package.
