## Description:

Bridges OpenClaw messaging channels to a persistent Claude Code CLI session in tmux so users can start, stop, monitor, and route chat messages to Claude Code with approval handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlhad](https://clawhub.ai/user/zlhad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to control a local Claude Code terminal session from OpenClaw chat channels, including mobile or group-chat workflows. It is useful when a user wants persistent remote access to Claude Code commands, approvals, and session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trusted chat participants can remotely drive a local Claude Code terminal, including actions that may run commands or change files after approval.

Mitigation: Install only for trusted channels, avoid sensitive repositories and group chats unless access is tightly controlled, and review every approval as permission for local terminal activity.

Risk: Broad message passthrough and raw history access can expose sensitive terminal output or repository context.

Mitigation: Limit who can access the chat channel, avoid sending secrets, and review transcript and history permissions before use.

Risk: Weak session isolation or generic key injection can route unintended input to a persistent terminal session.

Mitigation: Review session ID handling, CLAUDE_BIN launch behavior, and key injection behavior before deploying the skill.

## Reference(s):

- [CC-Bridge Usage Guide](references/usage.md)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown and plain text with shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes chat input to a local Claude Code CLI session and returns captured terminal output, including approval prompts and recent history.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
