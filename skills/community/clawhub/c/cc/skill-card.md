## Description:

Claude Code relay via tmux for starting sessions, forwarding messages, and reading output from Telegram or another OpenClaw channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artwalker](https://clawhub.ai/user/artwalker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to relay chat messages into an existing Claude Code session, manage tmux-backed project sessions, and inspect recent session output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay mode forwards ongoing chat messages to Claude Code, which may expose unrelated or sensitive messages.

Mitigation: Use relay mode only in a dedicated chat or channel, and stop it with /cc off when the session is finished.

Risk: Session output may be written to local logs.

Mitigation: Use the skill only on hosts and projects where local logging is acceptable, and review or remove logs according to local retention practices.

Risk: The selected project is accessible to Claude Code while the relay session is active.

Mitigation: Start sessions only for intended project directories and avoid enabling the relay for sensitive repositories unless that access is explicitly acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artwalker/skills/cc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell command invocations and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return incremental Claude Code session output; long output is summarized with guidance to use /cc tail.]

## Skill Version(s):

2.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
