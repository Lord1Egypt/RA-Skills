## Description:

DC power flow analysis for power systems, including DC approximation, susceptance matrix construction, line-flow and loading calculations, and sensitivity analysis on transmission networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power-system engineers use this skill to guide DC power-flow calculations, construct susceptance matrices from MATPOWER-style bus and branch data, calculate line flows, and reason about line loading and OPF constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Python helper reads local MATPOWER-style network data and depends on numpy.

Mitigation: Run the helper only on intended local input files and install numpy in a controlled environment.

Risk: DC power flow is a linearized approximation and may omit effects that matter in AC power-flow studies.

Mitigation: Review outputs against the intended engineering use case and validate critical decisions with appropriate power-system analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/energy-market-pricing-dc-power-flow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local Python helper that expects MATPOWER-style network JSON and numpy.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
