## Description:

Manage ClickUp tasks, docs, time tracking, comments, chat, and search via official MCP. OAuth authentication required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pvoo](https://clawhub.ai/user/pvoo)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to connect an agent to ClickUp through the official MCP server for workspace search, task management, comments, time tracking, chat, and docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to extract and persist a long-lived ClickUp access token from another application's credential store.

Mitigation: Protect CLICKUP_TOKEN like a password, store it with restrictive permissions or a secret manager, and avoid committing or syncing environment files.

Risk: Connected agents may receive ClickUp read and write abilities over sensitive workspace data.

Mitigation: Review the ClickUp workspace sensitivity before installing, grant access only when the requested abilities are acceptable, and revoke or rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pvoo/skills/clickup-mcp)
- [ClickUp](https://clickup.com)
- [ClickUp MCP Documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [ClickUp MCP Supported Tools](https://developer.clickup.com/docs/mcp-tools)
- [ClickUp API Reference](https://clickup.com/api)
- [Feedback / Allowlist Request](https://feedback.clickup.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and CLICKUP_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
