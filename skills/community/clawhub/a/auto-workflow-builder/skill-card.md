## Description:

Create and manage automated workflows visually with drag-and-drop triggers, actions, conditions, and integrations without coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and automation builders use this skill to design no-code workflows that connect schedules, webhooks, APIs, databases, notifications, and cloud actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflows may contact external services or modify remote systems through schedules, webhooks, APIs, databases, messaging tools, or AWS Lambda.

Mitigation: Review every trigger, action, destination, and credential before running or scheduling a workflow.

Risk: The artifact references a workflow.sh implementation that is not included.

Mitigation: Confirm the implementation source and safeguards before relying on generated or suggested workflow commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/auto-workflow-builder)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes workflow-building steps and command examples; the referenced workflow.sh implementation is not included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
