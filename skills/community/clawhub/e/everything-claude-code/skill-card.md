## Description:

Provides performance optimization guides and best practices for Claude AI agents, including CLI tools and Anthropic API integration details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill as a Claude Code toolkit and knowledge base for agent performance optimization, CLI workflows, hooks, commands, MCP configuration, security scanning, and Anthropic API integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit can auto-load hooks, persist local session and tool observations, and influence future agent sessions.

Mitigation: Review and disable wildcard observation plus SessionStart and SessionEnd hooks unless local memory capture is explicitly desired.

Risk: Optional installers and MCP server configurations may run third-party code or expand the agent's tool surface.

Mitigation: Avoid curl-to-bash installation, pin MCP packages before enabling them, and enable only the MCP servers needed for the project.

Risk: Configured MCP servers may require API credentials or other sensitive tokens.

Mitigation: Use narrowly scoped API tokens and keep credentials outside committed configuration files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/npjameszheng1125-netizen/skills/everything-claude-code)
- [Root Skill Definition](artifact/SKILL.md)
- [Everything Claude Code README](artifact/README.md)
- [Hooks Guide](artifact/hooks/README.md)
- [MCP Server Configurations](artifact/mcp-configs/mcp-servers.json)
- [Security Scan Skill](artifact/skills/security-scan/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes agent, command, hook, MCP, rule, and skill configuration content for Claude Code and related agent harnesses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
