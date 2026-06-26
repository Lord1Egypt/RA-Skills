# Free Energy Example — Ligand Binding to ISPETase (8H5K)

> This example shows how to set up a free energy calculation for a ligand binding to ISPETase.

## Required Inputs (not included — prepare before running)

1. **Protein structure:** Use ISPETase from `examples/ispetase/`
2. **Ligand:** PET dimer/trimer substrate (generate SMILES → 3D → parameterize)
3. **Docked complex:** Protein-ligand docking result (AutoDock Vina / Smina)

## Quick Setup

```bash
# 1. Parameterize ligand with acpype
# (requires ligand.mol2 from docking)
acpype -i ligand.mol2 -o gmx

# 2. Run free energy calculation
bash scripts/advanced/freeenergy.sh \
    --complex complex.pdb \
    --ligand ligand.mol2 \
    --method TI \
    --windows 13
```

## ISPETase-Specific Notes

- **Binding pocket:** Catalytic triad S160/D206/H237
- **Substrate:** PET trimer (2-hydroxyethyl terephthalate dimer) — SMILES: `O=C(OCC)OC1=CC=C(C=C1)C(=O)OCCO`
- **Key interactions:** Substrate carbonyl with S160 nucleophile
- **Suggested docking:** Use Smina with the catalytic pocket as search box

## Expected Outputs

- ΔG_bind ± error (kJ/mol)
- BAR analysis plot
- Per-window convergence check
- Free energy report
