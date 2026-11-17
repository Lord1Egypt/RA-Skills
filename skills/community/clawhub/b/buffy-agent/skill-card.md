## Description:

Buffy is a free HTTP client skill for creating and tracking habits, todo items, routines, reminders, and daily briefings through the Buffy API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phantue2002](https://clawhub.ai/user/phantue2002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage personal habits, todo tasks, routines, reminders, and progress summaries from chat or agent workflows. Integrators can optionally enable Buffy hooks for reminder dispatch and markdown observability logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked the release suspicious because it contains unrelated unpinned skill-discovery and global install examples.

Mitigation: Review, pin, and explicitly approve any npx skill-discovery or global install command before use.

Risk: Optional Buffy hooks can persist user messages, replies, reminders, and errors to local markdown logs.

Mitigation: Enable hooks only where log location, retention, access controls, and privacy requirements are defined.

Risk: The skill depends on a Buffy API key and sends user routine, habit, task, and reminder content to an external HTTPS API.

Mitigation: Provide a scoped BUFFY_API_KEY, avoid logging secrets, and use the skill only in environments approved for the external Buffy endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phantue2002/skills/buffy-agent)
- [Buffy API base endpoint](https://api.buffyai.org)
- [Buffy CLI repository](https://github.com/phantue2002/buffy-cli)
- [Buffy CLI releases](https://github.com/phantue2002/buffy-cli/releases)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, and API call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BUFFY_API_KEY and outbound HTTPS access to the configured Buffy endpoint.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
