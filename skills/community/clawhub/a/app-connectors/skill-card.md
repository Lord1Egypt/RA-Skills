## Description:

Connect your AI agent to 1000+ apps - discover tools, manage OAuth connections, execute actions, and provide a self-service connector dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ts-sz](https://clawhub.ai/user/ts-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent discover Composio-backed app tools, manage OAuth connections, list connected apps, and execute actions in connected third-party services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad Composio-mediated access to connected third-party apps.

Mitigation: Use a project-scoped COMPOSIO_API_KEY, limit connected apps to the operational need, and avoid letting the agent search unrelated secret stores.

Risk: The security summary says the skill does not clearly require user confirmation for side-effecting actions.

Mitigation: Require explicit approval before sends, writes, deletes, disconnects, or bulk actions in external services.

## Reference(s):

- [Composio Docs](https://docs.composio.dev)
- [ClawHub App Connectors skill page](https://clawhub.ai/ts-sz/skills/app-connectors)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project-scoped COMPOSIO_API_KEY and active user-approved OAuth connections before side-effecting tool execution.]

## Skill Version(s):

5.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
