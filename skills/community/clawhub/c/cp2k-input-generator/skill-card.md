## Description: <br>
Generates CP2K input files (.inp) for quantum chemistry calculations from structure files or CP2K outputs, covering calculation types such as energy, geometry optimization, molecular dynamics, frequency analysis, NEB, and methods including DFT, QMMM, and MM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirutong](https://clawhub.ai/user/sirutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational chemists, and materials researchers use this skill to create CP2K input files from molecular or crystal structures and requested simulation settings. It helps select CP2K sections and parameters for supported workflows such as single-point energy, optimization, molecular dynamics, frequency analysis, NEB, DOS, band structure, and QMMM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary and guidance appear inconsistent with the CP2K skill content. <br>
Mitigation: Use evidence.security as the authoritative scan result, but verify the publisher, version, and release package before deployment when provenance matters. <br>
Risk: Generated CP2K inputs may contain unsuitable simulation parameters for a specific system. <br>
Mitigation: Review generated input files against CP2K documentation and validate parameters such as charge, multiplicity, cutoff, basis set, periodicity, and k-points before running calculations. <br>


## Reference(s): <br>
- [CP2K Input Reference](references/cp2k_input_reference.md) <br>
- [CP2K Official Documentation](https://www.cp2k.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/sirutong/cp2k-input-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CP2K input code blocks, optional shell commands, and generated .inp file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a CP2K input file such as function.inp when the agent has file-write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
