## Description:

Monitor the Claude API for outages and latency spikes with Telegram alerts, status checks, latency probes, and recovery notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chapati23](https://clawhub.ai/user/chapati23)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure local Claude API monitoring, send Telegram alerts, and track status incidents and latency spikes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation creates persistent cron jobs and unsafe crontab handling may affect unrelated scheduled tasks.

Mitigation: Review and back up crontab before installing, and verify any uninstall or update touches only the intended watchdog entries.

Risk: Telegram and OpenClaw gateway tokens are stored in a local environment file.

Mitigation: Install only on a trusted machine, keep the env file permission-restricted, and rotate tokens if exposure is suspected.

Risk: The skill runs background checks every 15 minutes and sends outbound Telegram and status/probe requests.

Mitigation: Confirm the scheduled monitoring cadence and outbound notification behavior are appropriate for the deployment environment before enabling cron jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chapati23/skills/claude-watchdog)
- [ClawHub publisher profile](https://clawhub.ai/user/chapati23)
- [Anthropic status page](https://status.claude.com)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive setup writes local configuration, installs scheduled checks, and sends Telegram status or latency alerts.]

## Skill Version(s):

1.2.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
