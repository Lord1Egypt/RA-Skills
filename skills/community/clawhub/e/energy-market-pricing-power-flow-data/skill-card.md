## Description:

Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a reference for parsing MATPOWER-style power network JSON data, including bus, generator, branch, reserve, and load fields for power flow analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to open local power-grid JSON files.

Mitigation: Use it only with files the user intends the agent to analyze.

## Reference(s):

- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf)
- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/energy-market-pricing-power-flow-data)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on local MATPOWER-style JSON network data and parsing patterns.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
