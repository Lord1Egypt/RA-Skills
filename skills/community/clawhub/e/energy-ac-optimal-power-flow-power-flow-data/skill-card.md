## Description:

Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power systems engineers use this skill to parse MATPOWER-style network JSON data, map buses, generators, and branches, compute load, and understand reserve fields for power-flow analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read local power-network JSON files that contain sensitive operational or planning data.

Mitigation: Use it only with network data approved for analysis in the agent environment.

Risk: Large network files can consume unnecessary time and context if handled with line-oriented inspection.

Mitigation: Use structured JSON parsing and summary counts before deeper analysis, as described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/energy-ac-optimal-power-flow-power-flow-data)
- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on local MATPOWER-style JSON network data and topology concepts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
