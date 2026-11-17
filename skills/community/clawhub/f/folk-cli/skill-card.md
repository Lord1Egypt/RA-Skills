## Description:

Use folkctl to inspect and update folk.app CRM data through its REST API, covering people, companies, groups, members, custom fields, deals, custom objects, users, notes, tasks, interactions, legacy reminders, webhooks, and official MCP setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-edel](https://clawhub.ai/user/j-edel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and modify Folk CRM records through folkctl, with dry-run guidance for creates, updates, deletes, webhook setup, task management, and MCP configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful Folk CRM API key is routed through a globally installed third-party CLI with broad read and mutation abilities.

Mitigation: Install only if the pinned folkctl source is trusted, verify the CLI version before setting FOLK_API_KEY, and prefer a narrowly scoped or dedicated API key when available.

Risk: Create, update, delete, and field-option operations can change or remove CRM data.

Mitigation: Use --dry-run --json before mutations, summarize the exact resource, method, path, and body, and require explicit user confirmation before destructive commands.

Risk: Unexpected authentication failures or account activity may indicate an invalid, overexposed, or compromised Folk API key.

Mitigation: Ask the user to verify or rotate FOLK_API_KEY without pasting secrets into chat, avoid storing the token unless needed, and rotate it if unexpected activity appears.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-edel/skills/folk-cli)
- [folkctl repository](https://github.com/j-edel/folkctl)
- [Folk reminders-to-tasks migration guide](https://developer.folk.app/migrations/reminders-to-tasks)
- [Folk MCP tools reference](https://developer.folk.app/mcp/tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs often direct the agent to use folkctl --json, dry-run mutations before execution, and avoid printing FOLK_API_KEY.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
