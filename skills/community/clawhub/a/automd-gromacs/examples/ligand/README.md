# Ligand-Protein Complex Example — PET Substrate with ISPETase (8H5K)

> Set up and simulate a PET substrate bound to ISPETase.

## Prerequisites

1. **ISPEtase structure:** `examples/ispetase/setup/` (equilibrated)
2. **PET substrate:** Generate from SMILES, dock to catalytic pocket
3. **Docking software:** AutoDock Vina / Smina

## Step 1: Prepare Ligand

```bash
# Generate PET trimer from SMILES (using Open Babel)
obabel -:"O=C(OCC)OC1=CC=C(C=C1)C(=O)OCCO" -opdb -O pet_trimer.pdb --gen3d

# Convert to MOL2 for docking
obabel pet_trimer.pdb -omol2 -O pet_trimer.mol2
```

## Step 2: Dock to ISPETase

```bash
# Using Smina
smina --receptor ispetase.pdbqt \
      --ligand pet_trimer.pdbqt \
      --center_x 10 --center_y 5 --center_z 15 \
      --size_x 20 --size_y 20 --size_z 20 \
      --out docked.pdbqt
```

## Step 3: Run Ligand MD

```bash
bash scripts/advanced/ligand.sh \
    --receptor ispetase.pdb \
    --ligand docked_ligand.pdb \
    --output ligand_md
```

## Key ISPETase Binding Site Residues

- S160, D206, H237 — Catalytic triad
- Y87, W159, M161, W185, I208 — Substrate binding pocket
- F243, S244 — Oxyanion hole

## Expected Outputs

- Equilibrated complex (NPT)
- Production trajectory
- MM-PBSA binding energy
- Per-residue decomposition
