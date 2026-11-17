## Description:

Entrepreneur PM Framework helps managers route AI-agent work, align task goals, require relevant skill use, and capture lessons from completed tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevercrab321-svg](https://clawhub.ai/user/forevercrab321-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent-team managers use this skill to prepare structured task packages, select appropriate agents, define success criteria, enforce relevant skill use, and record operational lessons after completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes sensitive Shopify admin access patterns.

Mitigation: Remove or restrict the Shopify token path before use, and require explicit approval for any production store mutation.

Risk: The skill encourages persistent lessons and skill updates that could alter future agent behavior.

Mitigation: Require review before writing persistent lessons or modifying any skill files.

Risk: Agent routing may grant broad tool or secret access to subagents.

Mitigation: Limit subagent secret and tool access by role before delegating tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/forevercrab321-svg/skills/entrepreneur-pm)
- [Agent Capabilities Matrix](artifact/references/agent-capabilities.md)
- [Task Package Examples](artifact/references/task-examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown task packages, checklists, routing recommendations, and review templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, tool choices, and direct-operation instructions that should be reviewed before use in production systems.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
