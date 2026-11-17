## Description:

Generate photorealistic rendering scripts for PyMOL and UCSF ChimeraX to create publication-quality molecular visualizations with ray tracing, depth of field, ambient occlusion, and cinematic lighting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhaosu2024](https://clawhub.ai/user/renhaosu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational biologists, and visualization specialists use this skill to generate PyMOL or ChimeraX scripts for publication-quality protein structure images and presentation visuals. It is intended for visual rendering workflows, not routine structural analysis or measurement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PyMOL or ChimeraX command files may include unsanitized user input.

Mitigation: Use trusted, simple PDB IDs and file paths, inspect generated .pml or .cxc files before opening them, and add target-specific quoting and validation before broader use.

Risk: The script generator can write output outside the intended workspace when given unsafe paths.

Mitigation: Avoid absolute paths and traversal segments, keep outputs in a controlled workspace, and add workspace-only output containment and overwrite protection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renhaosu2024/skills/3d-molecule-ray-tracer)
- [PyMOL](https://pymol.org/)
- [UCSF ChimeraX](https://www.cgl.ucsf.edu/chimerax/)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Generated PyMOL .pml or ChimeraX .cxc command script with console guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static-image rendering scripts; PyMOL or ChimeraX must be installed separately.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
