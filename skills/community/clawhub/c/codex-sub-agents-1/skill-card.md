## Description:

Use OpenAI Codex CLI for coding tasks, including code review, CI fixes, refactoring, feature implementation, and Clawdbot delegation to Codex as a subagent or direct tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucanh08](https://clawhub.ai/user/phucanh08)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route coding work to Codex CLI, configure Clawdbot integration patterns, and produce commands or configuration for code review, refactoring, CI repair, and feature implementation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous coding-agent execution can modify files or run commands in sensitive repositories.

Mitigation: Use read-only or approval-gated modes by default, reserve `--full-auto` for isolated trusted workspaces, and review diffs before accepting changes.

Risk: Credential or profile reuse can expose private repository context, screenshots, logs, or API keys.

Mitigation: Redact secrets and sensitive artifacts before sharing them with agent workflows, and restrict use to appropriate authenticated workspaces.

Risk: Mutable MCP package execution can change behavior between runs.

Mitigation: Pin MCP server packages and review MCP configuration before enabling tool access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phucanh08/skills/codex-sub-agents-1)
- [Codex CLI Overview](https://developers.openai.com/codex/cli)
- [Codex CLI Features](https://developers.openai.com/codex/cli/features)
- [Codex CLI Reference](https://developers.openai.com/codex/cli/reference)
- [Slash Commands Guide](https://developers.openai.com/codex/cli/slash-commands)
- [AGENTS.md Spec](https://agents.md)
- [Codex GitHub](https://github.com/openai/codex)
- [DeepWiki MCP Endpoint](https://mcp.deepwiki.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON5, and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing CLI usage guidance, integration patterns, and configuration snippets for agent workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
