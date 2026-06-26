# Official Photogeneration Coupling Template

This is a topic-neutral workflow for coupling optical absorption to carrier generation in COMSOL Semiconductor models.

## Required User Configuration

- Active generation domains or selections.
- Passive optical domains, contacts, or boundaries.
- Wavelength, spectrum, optical intensity, and polarization.
- Absorption or electromagnetic power-density expression and units.
- Internal quantum efficiency or other conversion assumptions.
- Validation threshold for power balance or source-term conservation.

## Generic Workflow

1. Build or load the optical model.
2. Compute the volumetric absorbed power density in configured active domains.
3. Convert absorbed power to generation rate using a user-approved expression.
4. Assign generation only to configured active semiconductor domains.
5. Run dark equilibrium, illuminated equilibrium, dark bias sweep, and illuminated bias sweep as separate staged solves when needed.
6. Export current, generation integrals, absorbed power, carrier density, band edges, and convergence logs.

## Checks

- Source expression has units of `1/(m^3*s)` when used as carrier generation.
- Integrated generation is physically consistent with absorbed optical power.
- Passive or metallic domains do not accidentally receive carrier generation.
- Bias polarity and operating region are defined from the user's configured project, not from this package.
- Any simplified or uniform source term is labeled as a debug model unless validated for the configured project.
