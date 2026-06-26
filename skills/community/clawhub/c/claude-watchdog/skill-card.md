## Description: <br>
Monitor the Claude API for outages and latency spikes with rich Telegram alerts. Status monitoring, latency probes, and automatic recovery notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapati23](https://clawhub.ai/user/chapati23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Claude Watchdog to monitor Anthropic Claude API status and latency, receive Telegram alerts, and track recovery without manually checking service health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Telegram and OpenClaw gateway tokens in a local environment file. <br>
Mitigation: Keep the env file owner-only, use a dedicated Telegram bot or chat where possible, and avoid exposing gateway token command output. <br>
Risk: The setup installs cron checks that run every 15 minutes and send outbound status and alert requests. <br>
Mitigation: Review the installed crontab after setup and run the uninstall option when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chapati23/claude-watchdog) <br>
- [Claude status page](https://status.claude.com) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup instructions, cron-based monitoring behavior, Telegram alert text, and status or latency logs.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
