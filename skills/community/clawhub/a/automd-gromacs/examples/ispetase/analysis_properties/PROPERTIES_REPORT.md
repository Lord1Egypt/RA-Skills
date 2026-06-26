# Extended Protein Properties Report

## Dipole Moment
- File: `dipoles.xvg` — Total dipole moment (Debye) vs time
- File: `epsilon.xvg` — Dielectric constant estimate
- Interpretation: Large fluctuations indicate conformational changes

## Electrostatic Potential
- File: `potential.xvg` — Potential along box Z-axis (mV)
- Use: Identify charged patches, membrane potential

## Free Volume
- File: `freevolume.xvg` — Molecular and van der Waals volumes
- Interpretation: >0.25 = flexible, <0.20 = rigid

## Water Ordering (h2order)
- File: `h2order.xvg` — Water molecule orientation around protein
- Interpretation: High order near hydrophobic surfaces, low near charged

## Minimum Distance
- File: `mindist.xvg` — Closest contact distance between groups
- Use: Monitor binding/unbinding events, steric clashes

---
Generated: $(date)
