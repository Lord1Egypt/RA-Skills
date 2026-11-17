## Description:

Install, configure, and operate CronCopilot, a Python-based scheduled task management system for cron jobs, scripts, monitoring, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eden2f](https://clawhub.ai/user/eden2f)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install CronCopilot, manage scheduled tasks and scripts, monitor execution history, configure alerts, and troubleshoot failed or stuck jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create or modify scheduled jobs that run scripts on a recurring basis.

Mitigation: Review each proposed job schedule, script path, runtime user, timeout, retry behavior, and rollback step before enabling it.

Risk: Daemon or service setup can make CronCopilot persist across sessions or system restarts.

Mitigation: Inspect generated service files, startup entries, PID paths, and stop commands before enabling daemon, systemd, launchd, or WSL2 startup modes.

Risk: Package installation and upgrades can change the local runtime environment.

Mitigation: Use pinned releases and isolated virtual environments, and test upgrades before restarting the scheduler.

Risk: Alert configuration examples include SMTP credentials stored in configuration files.

Mitigation: Store credentials in a secret manager or a tightly permissioned file rather than ordinary YAML config.

Risk: Force deletion options may remove task registrations or script files.

Mitigation: Confirm the exact task or script target before using force removal or file deletion options.

## Reference(s):

- [CronCopilot Detailed Reference](artifact/REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/eden2f/skills/cron-copilot-ops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, command sequences, and configuration examples for local scheduled task management.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
