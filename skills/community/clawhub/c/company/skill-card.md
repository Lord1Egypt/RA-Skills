## Description:

Build an agent-powered organization by mapping functions to skills and iterating on structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, business operators, and developers use this skill to plan an agent-assisted company structure, map business functions to agent skills, sequence rollout, and define oversight checkpoints before expanding automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-critical functions such as finance, legal, HR, customer-facing, or publishing workflows may be delegated before sufficient controls are in place.

Mitigation: Define explicit scoped tools, human approval points, rollback criteria, and audit logs before allowing agents to operate in those workflows.

Risk: Agent scope may expand beyond its mandate as company workflows evolve.

Mitigation: Use the skill's iteration protocol to review scope regularly, track overrides and exceptions, and return to full human oversight when critical errors or rising override rates appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/company)
- [Common Functions to Skills Mapping](artifact/functions.md)
- [Iteration Protocol](artifact/iteration.md)
- [Organizational Patterns for Agent Companies](artifact/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with tables and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include function-to-skill mappings, rollout phases, boundaries, human checkpoints, tracking templates, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
