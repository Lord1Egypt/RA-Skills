## Description:

Helps agents manage Asana tasks, projects, workspaces, users, and webhooks through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to find and manage Asana work items and projects, or set up approved workflow automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration can read or change data in a connected Asana account.

Mitigation: Prefer OAuth and least-privilege access; start with read-only operations and confirm the account, connection, and intended change before writes.

Risk: Functions, triggers, destinations, and webhooks can keep running or forwarding data after setup.

Mitigation: Obtain explicit approval for each automation and destination, review its recipient and scope, and remove it when no longer needed.

## Reference(s):

- [Asana API Documentation](https://developers.asana.com)
- [Asana API Reference](https://developers.asana.com/reference)
- [Maton](https://maton.ai)
- [Maton Documentation](https://docs.maton.ai)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Scheduled Trigger Reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asana operations use the user's authorized connection; writes require confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
