## Description:

Configure, verify, repair, or minimize Dataify MCP for Claude Desktop, Codex, Cursor, Windsurf, or another MCP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a minimal Dataify MCP tool set, inspect or repair existing MCP configuration, and verify protocol readiness before continuing normal work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Dataify API token can be persisted in MCP client configuration URLs or backup files.

Mitigation: Use a narrowly scoped token, write configuration only when needed, keep backups protected, and rotate the token if it has already been stored in readable files.

Risk: Bundled scripts can run authenticated Dataify scraping or task workflows beyond MCP setup.

Mitigation: Review the included scripts before installation and execute workflow tools only with explicit target, scope, and credit expectations.

Risk: The authoritative security verdict is suspicious because setup behavior and bundled workflow behavior are not fully aligned.

Mitigation: Treat installation as a manual-review release and keep the selected MCP preset as narrow as the task permits.

## Reference(s):

- [Dataify documentation](https://doc.dataify.com)
- [Dataify support](https://www.dataify.com/)
- [Tool presets](references/tool-presets.md)
- [Dataify MCP skill page](https://clawhub.ai/dataify-server/skills/dataify-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce redacted configuration previews and protocol verification results.]

## Skill Version(s):

1.1.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
