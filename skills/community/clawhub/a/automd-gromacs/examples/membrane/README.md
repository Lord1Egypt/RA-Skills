# Membrane Protein Example

> ISPETase (8H5K) is a soluble enzyme — this example shows a generic membrane protein workflow.

## For ISPETase Users

ISPETase is soluble and does not require membrane simulation. For membrane protein MD, use the workflow below with a membrane protein of interest (e.g., GPCR, ion channel, transporter).

## Generic Membrane Protein Workflow

```bash
# 1. Prepare membrane with INSANE
python2 insane.py -o membrane.gro -p POPC -x 10 -y 10 -z 8 -l POPC

# 2. Insert protein into membrane
bash scripts/advanced/membrane.sh \
    --input protein.pdb \
    --membrane POPC \
    --temperature 310
```

## Notes

- Use CHARMM36 force field for membrane proteins
- Temperature: 310 K (physiological)
- Pressure coupling: semi-isotropic (separate XY and Z)
- Typical membrane types: POPC (mammalian), POPE (bacterial), DPPC (gel phase)
