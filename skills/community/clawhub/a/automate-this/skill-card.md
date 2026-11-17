## Description:

Part of the Overpowered skill suite. Transform a described human/business process into an executable automation design by separating deterministic steps, agentic reasoning, existing systems, and human gates; define triggers, data, decisions, exceptions, controls, and verification. Use when the goal is to automate a process, not merely understand it or interview the user about it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and automation designers use this skill to turn rough business-process descriptions, SOPs, forms, spreadsheets, emails, or diagrams into an implementation-ready automation design with clear interfaces, controls, failure behavior, and completion evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated automation designs may describe side effects, permissions, external-system changes, or approval gates that affect real workflows.

Mitigation: Review each design before implementation, especially external-system access, required permissions, side effects, and human approval criteria.

Risk: Ambiguous policies or incomplete process branches could be converted into automation requirements too early.

Mitigation: Keep unresolved policies and exceptions behind explicit human or knowledge-resolution gates until the process owner confirms them.

## Reference(s):

- [Implementation Modes](references/implementation-modes.md)
- [Overpowered skill suite](https://github.com/raguets/overpowered)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown process design with a step table and optional Mermaid or BPMN-like pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces design guidance only; generated automation plans should be reviewed before implementation.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
