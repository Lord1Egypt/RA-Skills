## Description:

BrainASLab analyzes FreeSurfer cortical stats files to compute cortical asymmetry indices and produce CSV results and plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxx536](https://clawhub.ai/user/xxxx536)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to process FreeSurfer lh.aparc.stats and rh.aparc.stats files, compute cortical asymmetry indices for thickness, area, and volume, and collect CSV and plot outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted input paths could alter the generated MATLAB batch script and execute unintended MATLAB or system commands.

Mitigation: Use only trusted FreeSurfer stats file paths until path escaping or a safer invocation strategy is implemented.

Risk: MATLAB failures are not handled explicitly, so missing or failed outputs may be returned without a clear execution error.

Mitigation: Check MATLAB availability and verify expected CSV and plot outputs before relying on results.

## Reference(s):

- [BrainASLab ClawHub skill page](https://clawhub.ai/xxxx536/skills/brainaslab)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [JSON-like object containing CSV and plot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATLAB available in PATH.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
