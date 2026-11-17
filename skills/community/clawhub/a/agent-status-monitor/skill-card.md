## Description:

Monitors local AI development agents such as Claude Code, OpenCode, OpenClaw, and Cursor by checking process status, session files, and recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willin](https://clawhub.ai/user/willin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check whether local AI coding agents are running, active, idle, or unavailable, including session counts and basic status details. It supports local workstation monitoring and optional Telegram command reporting for the same status view.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local agent status, session counts, and local paths may reveal development activity or host details.

Mitigation: Review status output before sharing it and install only where exposing local agent activity is acceptable.

Risk: The Telegram command can expose local agent and host status in groups or shared chats.

Mitigation: Use the command only in private chats or add an allowlist/private-chat restriction before enabling it.

Risk: Reference commands can reveal prompt history or search broadly across the home directory.

Mitigation: Do not run prompt-history or home-wide search commands unless the output has been reviewed for sensitive data.

Risk: Unpinned installer commands can retrieve changing remote package contents.

Mitigation: Prefer the ClawHub install path or a pinned installer version.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willin/skills/agent-status-monitor)
- [Agent Commands Reference](references/agent-commands.md)
- [Telegram Command Usage](telegram-commands/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Terminal text and Markdown status reports with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local process status, recent session file activity, session counts, and selected local paths; Telegram output is formatted as a Markdown code block.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
