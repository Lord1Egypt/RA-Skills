## Description:

Claude Agent helps OpenClaw plan, launch, monitor, and review Claude Code tasks through tmux sessions, hooks, and approval handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1neman](https://clawhub.ai/user/n1neman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to delegate coding tasks to Claude Code while keeping task planning, approval handling, monitoring, quality checks, and final reporting under OpenClaw supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables persistent OpenClaw supervision of Claude Code, which can affect projects and local configuration.

Mitigation: Install it only when that delegation is intended, review configuration changes before use, and remove the Claude Code Stop hook when the automation is no longer needed.

Risk: Auto mode can allow Claude Code to execute tools without prompting the operator.

Mitigation: Avoid auto mode unless that behavior is acceptable, and restrict Claude permissions to specific projects and commands.

Risk: Notifications and wake events may expose task context if optional summary or full-detail modes are enabled.

Mitigation: Keep event-only notification defaults for sensitive work and use trusted private channels before enabling summaries or approval details.

## Reference(s):

- [Claude Agent on ClawHub](https://clawhub.ai/n1neman/skills/claude-agent)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code CLI reference](references/claude-code-reference.md)
- [Security and Privacy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce prompts, approval decisions, execution reports, and local configuration guidance for Claude Code and OpenClaw workflows.]

## Skill Version(s):

2.1.0 (source: server release evidence and changelog, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
