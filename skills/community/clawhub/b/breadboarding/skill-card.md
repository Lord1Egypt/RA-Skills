## Description:

Breadboarding transforms workflow descriptions into affordance tables that show UI and code affordances, their wiring, and optional Mermaid visualizations for mapping existing systems or designing new ones from shaped parts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product engineers, and design reviewers use this skill to map existing workflows or design new systems by turning operator-centered flows, code paths, or shaped parts into Places, UI affordances, Code affordances, wires, returns, data stores, and optional Mermaid diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect project code when mapping an existing workflow.

Mitigation: Limit review to relevant project files and follow the workspace's normal access controls.

Risk: Affordance tables can be misleading if the generated wiring is not checked against the actual code or intended design.

Mitigation: Review the generated tables against source code or shaping requirements before using them for implementation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morpheis/skills/breadboarding)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown tables with optional Mermaid code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Places, UI Affordances, Code Affordances, Data Stores, and optional slice summaries or diagrams.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
