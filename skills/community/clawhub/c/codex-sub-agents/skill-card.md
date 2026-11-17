## Description:

Use OpenAI Codex CLI for coding tasks including code review, CI fixes, refactoring, feature implementation, and Clawdbot delegation to Codex CLI as a subagent or direct tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamsardo](https://clawhub.ai/user/adamsardo)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to route coding work to OpenAI Codex CLI for code review, bug fixes, CI repair, refactoring, feature implementation, and subagent-based coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to run Codex CLI with broad coding permissions and persistent credential or configuration access.

Mitigation: Use read-only or approval-required modes first, reserve --full-auto and --yolo for isolated trusted workspaces, and review changes to Codex or Clawdbot auth and configuration files.

Risk: MCP server configuration can extend the agent's access through third-party tools.

Mitigation: Pin or vet third-party MCP servers before enabling them.

## Reference(s):

- [OpenAI Codex CLI Overview](https://developers.openai.com/codex/cli)
- [OpenAI Codex CLI Features](https://developers.openai.com/codex/cli/features)
- [OpenAI Codex CLI Reference](https://developers.openai.com/codex/cli/reference)
- [OpenAI Codex Slash Commands Guide](https://developers.openai.com/codex/cli/slash-commands)
- [AGENTS.md Specification](https://agents.md)
- [OpenAI Codex GitHub Repository](https://github.com/openai/codex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Codex CLI commands, Clawdbot configuration examples, MCP setup guidance, and coding workflow recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
