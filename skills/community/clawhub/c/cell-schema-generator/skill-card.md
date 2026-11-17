## Description:

Generates complete CellOS-compatible YAML schemas from plain-text team or organization descriptions, including steward roles, scope boundaries, escalation rules, and coordination protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and organizational designers use this skill to convert plain-language team descriptions into CellOS cell schemas for AI-native organizational governance and coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated governance schemas may contain incorrect steward assignments, scope boundaries, escalation paths, or access assumptions if the input description is incomplete or inaccurate.

Mitigation: Review each generated schema with the responsible team before operational adoption, resolving TBD fields and validating access, escalation, and integrity responsibilities.

Risk: Schemas can describe AI-agent stewardship, memory, permissions, and escalation concepts that may affect real operational governance if adopted without review.

Mitigation: Treat the output as a draft governance artifact and require approval from accountable human owners before using it to guide operations.

## Reference(s):

- [CellOS Framework Overview](references/cellos-overview.md)
- [Minimal Cell Schema Template](templates/minimal-cell.yaml)
- [Cell Schema Generator on ClawHub](https://clawhub.ai/filipbl4gojevic/skills/cell-schema-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown containing a YAML schema and design notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated schemas may include TBD fields or assumptions when the user's organizational description is incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
