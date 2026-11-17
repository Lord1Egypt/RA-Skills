## Description:

Helps agents manage ClickUp tasks, project structures, users, and webhooks through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People managing ClickUp projects can ask an agent to find or update tasks and project structures, or configure approved webhooks and automations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the wrong account or granting unnecessary ClickUp access.

Mitigation: Confirm the account and connection with the user and authorize only the scopes needed for the task.

Risk: Writes, webhooks, triggers, and destinations may change data or establish ongoing data flows.

Mitigation: Prefer read-only calls and confirm each write and automation destination before enabling it.

Risk: A raw Maton API key can be exposed when used outside the CLI.

Mitigation: Prefer OAuth through the CLI; if a key is required, keep it out of logs, command lines, and persistent files.

## Reference(s):

- [ClickUp skill release](https://clawhub.ai/byungkyu/skills/clickup-api)
- [ClickUp API overview](https://developer.clickup.com/docs/Getting%20Started.md)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with commands, code examples, and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses and actions depend on the connected ClickUp account's permissions.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
