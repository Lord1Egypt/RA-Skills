## Description:

Task Management is a local task management skill for creating, querying, updating, deleting, recycling, and reporting on tasks through a CLI or optional web interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xfwgithub](https://clawhub.ai/user/xfwgithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and project operators use this skill to manage task lifecycles, including creation, assignment, status transitions, review handoffs, deletion, recycling overdue work, and dashboard statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional web interface can expose and change tasks over the network without login.

Mitigation: Run the web server only on localhost or behind authentication, and do not expose it on an untrusted network.

Risk: Task data may include sensitive business or personal information while the release has data-handling weaknesses.

Mitigation: Avoid storing sensitive data until API authentication, status validation, XSS handling, and database-permission issues are fixed.

Risk: Unverified installation sources or mutable downloads can increase supply-chain risk.

Mitigation: Prefer pinned, verified releases and review the local task database behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xfwgithub/skills/ai-task-management)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON task responses and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill manages local task records and can expose an optional web interface on a configured port.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact runtime files also reference 0.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
