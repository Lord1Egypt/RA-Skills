## Description:

Manage FlowMind goals, tasks, subtasks, notes, contacts, and tags through its REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fancygobot](https://clawhub.ai/user/fancygobot)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a FlowMind productivity workspace through natural-language agent guidance and REST API calls, including goals, tasks, notes, people, tags, focus lists, progress tracking, and meeting preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide delete actions for goals, tasks, notes, contacts, and tags.

Mitigation: Confirm the exact record title or identity before delete actions and prefer archiving or status changes when available.

Risk: The skill relies on a FlowMind API key and may access account productivity, contact, business, or financial planning data.

Mitigation: Install only when the publisher and FlowMind account context are trusted, and scope API-key use to the intended account.

## Reference(s):

- [FlowMind API Reference](references/api.md)
- [FlowMind Website](https://flowmind.life/)
- [FlowMind API Base URL](https://flowmind.life/api/v1)
- [FlowMind ClawHub Skill Page](https://clawhub.ai/fancygobot/skills/flowmind)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown with REST API endpoints, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FlowMind API key and can guide authenticated create, update, list, and delete operations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
