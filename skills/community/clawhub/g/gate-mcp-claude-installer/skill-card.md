## Description:

Installs selected Gate MCP servers and the Gate skills bundle for Claude Code, with guidance for configuration, authentication, and post-install verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to install Gate MCP endpoints, merge Claude MCP configuration, and optionally install the full Gate skills bundle. It is intended for setup and configuration, not for trading operations or market analysis execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer makes persistent changes to Claude Code MCP configuration and may replace existing Gate skill directories.

Mitigation: Back up ~/.claude.json and ~/.claude/skills/ before installation, and verify the resulting configuration and installed skills after the script completes.

Risk: The installer can fetch mutable remote code from GitHub and npm at install time.

Mitigation: Install only when the Gate publisher, remote services, and live source locations are trusted; review cloned skills and package versions before use.

Risk: Trading API secrets may be stored in Claude configuration if the user enters them during setup.

Mitigation: Avoid entering trading secrets unless needed, prefer narrowly scoped or read-only keys where possible, and keep secrets out of logs and shared output.

## Reference(s):

- [Gate Claude Installer MCP Specification](references/mcp.md)
- [Gate MCP](https://github.com/gate/gate-mcp)
- [Gate Skills](https://github.com/gate/gate-skills)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-mcp-claude-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce manual MCP configuration snippets when automatic installation cannot complete.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter: 2026.3.25-2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
