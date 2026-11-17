## Description:

Generates CP2K input files (.inp) for quantum chemistry calculations from structural files or CP2K outputs, covering workflows such as energy calculations, geometry optimization, molecular dynamics, frequency analysis, NEB, DFT, QMMM, and MM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirutong](https://clawhub.ai/user/sirutong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry researchers use this skill to generate and review CP2K .inp files from structure files, CP2K outputs, and calculation requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An existing .inp file could be overwritten when the skill or bundled script writes to the requested output path.

Mitigation: Confirm the output path before writing and preserve original structure and input files.

Risk: Advanced workflows such as NEB, frequency analysis, QMMM, MM, or CP2K-output reuse may need manual completion or correction.

Mitigation: Review generated sections and parameters against CP2K documentation and trusted examples before running production calculations.

Risk: Automatically selected basis sets, cutoffs, k-points, and SCF settings may not match the desired scientific accuracy or resource budget.

Mitigation: Validate parameter choices and resource estimates for the specific system before submitting the CP2K job.

## Reference(s):

- [CP2K Input Reference](references/cp2k_input_reference.md)
- [CP2K Official Documentation](https://www.cp2k.org/)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [CP2K .inp configuration text, often presented in Markdown with shell commands or written as an .inp file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a CP2K .inp file when an output path is specified; generated inputs should be reviewed before running CP2K.]

## Skill Version(s):

1.0.0 (source: server release metadata, README changelog dated 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
