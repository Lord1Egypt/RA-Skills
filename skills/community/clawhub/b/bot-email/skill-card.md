## Description:

Get an email address without your human. Use for testing signup flows, receiving verification codes, automating email workflows. Free.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-silhouette](https://clawhub.ai/user/claw-silhouette)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create bot email inboxes, read incoming messages, extract verification codes, and monitor email-driven workflows for testing and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles bot inbox contents, verification emails, codes, and API keys.

Mitigation: Use it only for accounts where sending these materials to BotEmail.ai is acceptable, treat API keys like passwords, and avoid high-value or regulated accounts.

Risk: The documented API supports deleting individual messages and clearing an inbox.

Mitigation: Require explicit user confirmation before deleting messages or clearing an inbox.

Risk: Dashboard URLs may expose access keys if shared.

Mitigation: Avoid sharing dashboard URLs that contain API keys or other credentials.

Risk: The optional MCP server adds executable third-party code to the environment.

Mitigation: Use the MCP server only from a pinned, reviewed commit in an isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claw-silhouette/skills/bot-email)
- [BotEmail.ai API Docs](https://botemail.ai/docs)
- [BotEmail.ai Dashboard](https://botemail.ai/dashboard)
- [BotEmail.ai MCP Server](https://github.com/claw-silhouette/botemail-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, JSON examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for HTTP API use, credential handling, inbox monitoring, and optional MCP setup.]

## Skill Version(s):

v1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
