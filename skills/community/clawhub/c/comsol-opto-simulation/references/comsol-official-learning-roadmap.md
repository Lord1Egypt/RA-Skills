# COMSOL Official Learning Roadmap

Use official COMSOL examples and documentation to confirm API names, physics interfaces, and solver patterns for the user's configured project.

## Useful Example Categories

| Category | Why It Helps |
| --- | --- |
| Optical wave or ray optics examples | Field setup, wavelength sweeps, absorption postprocessing |
| Semiconductor diode or photodiode examples | Contacts, generation, recombination, bias continuation |
| Heterojunction examples | Band offsets and interface boundary conditions |
| Heat transfer examples | Thermal boundaries and material property setup |
| Multiphysics examples | Staged coupling, segregated solvers, and result transfer |

## Workflow

1. Identify the physics modules needed by the user's configured project.
2. Locate official examples for those physics interfaces.
3. Export Model Java where possible to inspect feature tags and property keys.
4. Transfer only API patterns, not material defaults or example-specific parameters.
5. Validate with a minimal configured model before scaling to the full project.

## Notes

- COMSOL feature names vary by version and installed module.
- Treat official examples as API and solver references, not as a source of project parameters.
- Record COMSOL version, license modules, and any unavailable examples in the output log.
