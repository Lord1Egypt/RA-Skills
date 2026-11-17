## Description:

Your Claude Code wingman - orchestrate multiple Claude Code sessions across projects, monitor them all from WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yossiovadia](https://clawhub.ai/user/yossiovadia)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to delegate coding tasks to Claude Code sessions, monitor progress, and approve or deny session actions from chat or WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically approve trust and tool-permission prompts that normally require human review.

Mitigation: Install only for trusted use cases, run it in disposable or well-contained project environments, review approval requests carefully, and avoid auto mode for normal repositories.

Risk: The always approval path can allow repeated similar actions within a session.

Mitigation: Use always only when the project and action class are trusted; otherwise approve one request at a time or deny unsafe actions.

Risk: Background approvers and local approval files can affect live Claude Code sessions.

Mitigation: Treat approver processes and /tmp approval files as sensitive local automation, and stop monitoring or approval daemons when they are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yossiovadia/skills/claude-code-wingman)
- [Claude Code Wingman GitHub repository](https://github.com/yossiovadia/claude-code-wingman)
- [Usage guide](USAGE.md)
- [Helper library documentation](lib/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Claude Code CLI and tmux; jq is used by session and monitoring helpers.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
