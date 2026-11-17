## Description:

DeadClaw is an emergency stop skill for OpenClaw agents that can halt running agents, pause scheduled jobs, stop active sessions, log incidents, and provide status or restore guidance from chat, WebChat, phone shortcut, or watchdog triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kintupercy](https://clawhub.ai/user/kintupercy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use DeadClaw as an emergency control for OpenClaw deployments when agents appear runaway, suspicious, too costly, or need to be stopped from a remote surface. It also helps inspect current agent state and restore paused jobs or containers after the incident is reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad chat triggers and simple buttons can stop or restart OpenClaw resources without adequate authorization safeguards.

Mitigation: Use a namespaced admin-only trigger, restrict allowed senders and channels, and require confirmation for kill and restore actions.

Risk: The skill can stop agents, containers, sessions, cron jobs, and user services.

Mitigation: Install only where emergency-stop authority is intended, test with dry-run mode before live use, and protect cron backups.

Risk: Phone shortcuts may store Telegram bot tokens as long-lived credentials.

Mitigation: Treat shortcut tokens as secrets, limit who can access them, and rotate tokens if they are shared or exposed.

Risk: Overly broad process patterns can affect unintended processes.

Mitigation: Configure narrow OpenClaw-specific process patterns and review status output before live kill or restore flows when time allows.

## Reference(s):

- [ClawHub DeadClaw skill page](https://clawhub.ai/kintupercy/skills/deadclaw)
- [DeadClaw README](artifact/README.md)
- [iPhone shortcut setup guide](artifact/docs/iphone-shortcut-guide.md)
- [Android widget setup guide](artifact/docs/android-widget-guide.md)
- [ClawHub listing notes](artifact/docs/clawhub-listing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, status text, and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe or invoke local stop, status, watchdog, and restore actions when the host agent grants the requested authority.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
