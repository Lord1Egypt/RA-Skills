## Description:

Bridges OpenClaw chat channels such as QQ, Telegram, and WeChat to a persistent Claude Code CLI session running in tmux so users can start, monitor, control, and route messages to Claude Code from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlhad](https://clawhub.ai/user/zlhad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to operate a local Claude Code terminal session from supported chat channels, including choosing a working directory, using sandbox mode, sending prompts, relaying slash commands, and handling approval prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat users on connected channels can control a persistent local Claude Code terminal.

Mitigation: Install only for trusted chat users, restrict bot access, prefer sandbox mode or a low-privilege account, and avoid sensitive working directories.

Risk: Server security evidence reports a confirmed startup command-injection risk and session-collision concerns.

Mitigation: Fix these issues before use in shared, remote, or multi-user environments.

Risk: Peek and history commands can expose sensitive terminal or project output.

Mitigation: Treat session output as sensitive and limit use to channels and users authorized to view the underlying project.

Risk: Project-wide approvals can allow broader Claude Code actions than the user intended.

Mitigation: Avoid persistent project approvals unless the requested action and working directory are fully understood.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zlhad/skills/claude-code-bridge)
- [Claude Code Bridge usage guide](references/usage.md)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text or Markdown relayed from a Claude Code terminal session, with command output and code blocks when produced by Claude Code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal history, approval choices, status text, and truncated long-session output.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
