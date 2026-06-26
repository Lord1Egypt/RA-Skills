# COMSOL Convergence Diagnostics

Use this checklist for user-configured optical, semiconductor, thermal, or coupled COMSOL models. Do not assume any material stack, bias polarity, or default parameter set from this package.

## Pre-Solve Checks

- Confirm every layer/domain name in the JSON config maps to a COMSOL domain selection.
- Confirm active physics is assigned by configured role, not by a hard-coded material name.
- Confirm electrodes, passive layers, and active domains are intentionally included or excluded from each physics interface.
- Confirm units for thickness, mobility, doping, lifetime, thermal parameters, optical intensity, and source terms.
- Confirm all placeholders from the user's own project configuration are replaced before quantitative runs.

## Solver Triage

| Symptom | Likely Cause | First Diagnostic |
| --- | --- | --- |
| Equilibrium fails | Bad contacts, impossible band offsets, missing material values | Run zero-bias single-physics model |
| Bias sweep fails | Step too large or strong nonlinearity | Reduce bias step and use continuation |
| Optical solve fails | Mesh too coarse/fine or bad optical constants | Test one wavelength and one polarization |
| Thermal solve diverges | Source term or boundary condition inconsistent | Run steady heat transfer only |
| Coupled solve is unstable | Strong feedback between physics | Use segregated solve or staged coupling |

## Geometry And Mesh

- Refine material interfaces, contacts, and high-gradient source regions first.
- Use swept/mapped mesh for thin layers when aspect ratio is severe.
- Temporarily simplify the model to one active domain to isolate solver failure.
- Record mesh size, DOF estimate, and convergence status in output JSON.

## Physics Reasonableness

- Check sign and magnitude of fields, currents, heat fluxes, and integrated sources.
- Compare limiting cases: dark vs illuminated, zero source vs finite source, low vs high bias, low vs high temperature.
- Verify conservation checks such as absorbed optical power vs integrated generation when relevant.
- Report which parameters are measured, literature-sourced, assumed, or still unconfigured.

## Escalation Path

1. Fix obvious units and missing parameters.
2. Run a reduced single-physics model.
3. Run staged coupling with saved intermediate state.
4. Reduce sweep range or use continuation.
5. Revisit the physical model and boundary assumptions.
