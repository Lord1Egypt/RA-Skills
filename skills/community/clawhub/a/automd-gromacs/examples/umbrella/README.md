# Umbrella Sampling Example — PET Substrate Unbinding from ISPETase (8H5K)

> Pull a PET substrate out of the ISPETase binding pocket and compute the PMF.

## Required Inputs

1. **Equilibrated complex:** ISPETase + docked PET substrate (see `examples/ligand/`)
2. **Pull direction:** Along the substrate access channel (z-axis of binding pocket)
3. **Reaction coordinate:** Distance between substrate COM and catalytic S160 Cα

## Quick Setup

```bash
# Define pull groups in index file
gmx make_ndx -f complex.gro -o index.ndx

# Run umbrella sampling with auto-window setup
bash scripts/advanced/umbrella.sh \
    --input complex.gro \
    --topology topol.top \
    --pull-group1 "Protein" \
    --pull-group2 "LIG" \
    --pull-rate 0.01 \
    --window-spacing 0.1 \
    --windows 30
```

## ISPETase-Specific Notes

- **Pull distance:** ~2.0-3.0 nm (from binding pocket to bulk solvent)
- **Window force constant:** 1000 kJ/mol/nm²
- **Sample time:** 1-5 ns per window (for production)
- **Key residues lining channel:** Y87, W159, S160, M161, W185, I208
