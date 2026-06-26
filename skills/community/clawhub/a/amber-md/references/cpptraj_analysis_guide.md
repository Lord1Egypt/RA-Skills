# cpptraj Analysis Guide

## Recommended analysis order
1. Load topology
2. Load trajectory
3. Strip water and ions if appropriate
4. Apply `autoimage`
5. Compute RMSD
6. Compute RMSF

## Typical outputs
- RMSD time series
- RMSF per residue
- Radius of gyration
- Hydrogen-bond summaries

## Common pitfalls
- Using all atoms including solvent for RMSD
- Inconsistent masks between reference and trajectory
- Forgetting periodic imaging correction
