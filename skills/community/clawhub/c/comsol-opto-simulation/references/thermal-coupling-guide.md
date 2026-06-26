# Thermal And Multiphysics Coupling Guide

This guide is topic-neutral. It provides a structure for thermal or coupled thermal-electrical/optical simulations, but no material-specific constants.

## Required Configuration

- Geometry and layer/domain roles.
- Thermal conductivity, density, and heat capacity for each configured material.
- Heat sources: optical absorption, Joule heating, reactions, phase change, or user-defined source terms.
- Boundary conditions: convection, fixed temperature, radiation, heat flux, symmetry, or adiabatic boundaries.
- Temperature-dependent material models when the target metric depends on temperature.
- Failure, stability, or safety criteria from the user's own project.

## Generic Heat Source Checks

| Source | Required Input | Validation |
| --- | --- | --- |
| Optical absorption | Absorbed power density or imported optical result | Integral matches absorbed optical power |
| Joule heating | Current density and electric field | Sign and magnitude are plausible |
| External heating | Flux, volume source, or boundary source | Units and applied region are correct |
| Temperature feedback | Coefficients or fitted model | Model range covers simulated temperature |

## Boundary Checklist

- State the physical environment for every exposed boundary.
- Use measured thermal contact assumptions when possible.
- Test adiabatic, fixed-temperature, and convection limits if the heat path is uncertain.
- Report maximum temperature, average temperature, heat flux path, and sensitivity to boundary assumptions.

## Reporting Template

- Configured material table and sources.
- Heat-source expression and domain selection.
- Boundary conditions and ambient conditions.
- Solver sequence and convergence result.
- Temperature map, maximum temperature, and the user's configured acceptance criterion.

Do not reuse thermal constants, degradation thresholds, or illumination levels from this package as project facts.
