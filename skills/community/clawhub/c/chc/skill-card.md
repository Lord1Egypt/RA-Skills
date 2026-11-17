## Description:

OpenClaw manages Claude Code CLI sessions so an agent can start, message, persist, inspect, and close Claude Code sessions through ACP or PTY workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Claude Code CLI sessions from OpenClaw, especially for multi-turn coding work, multiple concurrent projects, and fallback PTY control when ACP is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or invokes an unpinned acpx CLI, which can change behavior across installs.

Mitigation: Review or pin the acpx package before installation and deployment.

Risk: The skill manages local Claude Code configuration and session files that may contain sensitive conversation history or credentials.

Mitigation: Treat Claude configuration and session files as sensitive, limit access to trusted users, and avoid sharing raw session data.

Risk: The troubleshooting guidance includes deleting an acpx configuration file.

Mitigation: Back up configuration files before deletion and prefer targeted edits when the invalid setting is known.

## Reference(s):

- [Claude Code CLI](https://docs.anthropic.com/claude-code)
- [Agent Client Protocol](https://github.com/agentclientprotocol)
- [Claude Code CLI Configuration Reference](references/config.md)
- [ClawHub Skill Page](https://clawhub.ai/linux2010/skills/chc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ACP commands, PTY interaction steps, session lifecycle guidance, and local configuration or session inspection instructions.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
