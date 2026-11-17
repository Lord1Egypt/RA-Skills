## Description:

Generate algorithmic visual art — flow fields, fractals, cellular automata, circle packing, wave patterns. SVG + PNG output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliot-onbox](https://clawhub.ai/user/eliot-onbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and creative agents use GenArt to generate deterministic procedural visual art as SVG or PNG files from configurable algorithmic patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output can overwrite files at paths writable by the current user.

Mitigation: Choose explicit output paths in a disposable or project-specific directory and review paths before running generation commands.

Risk: PNG generation may invoke a local SVG renderer, and SVG input handling is under-documented.

Mitigation: Use trusted SVG inputs for glitch transformations and review renderer availability and behavior before relying on PNG output.

Risk: Extreme size, count, iteration, layer, row, or column settings can create local resource pressure.

Mitigation: Keep dimensions and generation counts within practical limits, especially in automated agent workflows.

## Reference(s):

- [GenArt ClawHub release](https://clawhub.ai/eliot-onbox/skills/genart)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [SVG and PNG files with Markdown or shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are deterministic when a seed is supplied; PNG creation may depend on a local SVG renderer.]

## Skill Version(s):

2.0.0 (source: server release metadata, released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
