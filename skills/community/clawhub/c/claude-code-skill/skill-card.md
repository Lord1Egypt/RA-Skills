## Description:

Integrates MCP tool server orchestration, persistent state storage, and session synchronization utilities for OpenClaw and Claude Code workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderfga](https://clawhub.ai/user/enderfga)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to connect OpenClaw or Claude Code agents to configured MCP tool servers, persist agent state, and merge chat or configuration state across sessions and devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured MCP servers may run local commands and receive environment or config-provided credentials.

Mitigation: Use only pinned and reviewed MCP server packages, avoid runtime npx -y startup, run with a minimal environment, and keep real tokens out of shared config files.

Risk: Persistent storage and session synchronization can retain sensitive chat content, tool output, or regulated data.

Mitigation: Do not persist or sync secrets, regulated data, or sensitive chat/tool output until the package provides clearer controls and documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderfga/skills/claude-code-skill)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io/)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Zustand](https://github.com/pmndrs/zustand)
- [npm package](https://www.npmjs.com/package/openclaw-claude-code-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include MCP server configuration, API usage examples, and persistence or synchronization patterns.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
