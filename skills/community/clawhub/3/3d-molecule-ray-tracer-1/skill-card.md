## Description:

Generate photorealistic rendering scripts for PyMOL and UCSF ChimeraX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational science users use this skill to generate PyMOL or UCSF ChimeraX rendering scripts for publication, cover, presentation, or cinematic molecular visuals from a PDB ID or local structure file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PyMOL or ChimeraX scripts may embed unvalidated molecular input values into tool commands.

Mitigation: Use only trusted molecular inputs and inspect generated .pml or .cxc files before opening them in PyMOL or ChimeraX.

Risk: The script generator can overwrite arbitrary writable output paths.

Mitigation: Keep output filenames simple, write inside the current project directory, and add output-path containment plus overwrite protection before treating the skill as low-risk.

Risk: The release has a suspicious scanner verdict and requires review before installation or execution.

Mitigation: Review and scan the skill before deployment, and require strict validation and command escaping before broader use.

## Reference(s):

- [PyMOL](https://pymol.org/)
- [UCSF ChimeraX](https://www.cgl.ucsf.edu/chimerax/)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/3d-molecule-ray-tracer-1)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PyMOL .pml or ChimeraX .cxc script files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from command-line options for target software, PDB input, preset, style, resolution, lighting, effects, and output filename.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
