## Description: <br>
Emergency kill switch for OpenClaw agents that can halt running agents, pause scheduled jobs, kill active sessions, log incidents, and report status through message, WebChat, phone shortcut, or watchdog triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kintupercy](https://clawhub.ai/user/Kintupercy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and operators use DeadClaw to stop, monitor, and restore agent processes when autonomous agents run away, spend unexpectedly, make unauthorized network calls, or need an emergency shutdown from a phone, chat channel, or dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote triggers can grant broad shutdown and restore authority over OpenClaw agents. <br>
Mitigation: Install only where trigger channels are controlled, use namespaced trigger words, restrict authorized senders and channels, and test with --dry-run before enabling live actions. <br>
Risk: Phone shortcuts and messaging integrations can expose or misuse trigger paths if tokens or channels are not controlled. <br>
Mitigation: Avoid storing Telegram bot tokens in phone shortcuts when possible, restrict bot access, and rotate or revoke exposed credentials. <br>
Risk: Watchdog and restore behavior can stop or restart jobs in the target environment. <br>
Mitigation: Review the exact watchdog thresholds, restore behavior, crontab backups, and workspace settings in the deployed copy before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kintupercy/deadclaw) <br>
- [DeadClaw README](artifact/deadclaw/README.md) <br>
- [ClawHub Listing](artifact/deadclaw/docs/clawhub-listing.md) <br>
- [iPhone Shortcut Guide](artifact/deadclaw/docs/iphone-shortcut-guide.md) <br>
- [Android Widget Guide](artifact/deadclaw/docs/android-widget-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown status, confirmation, setup, and recovery guidance with shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute kill, status, restore, or watchdog scripts; supports dry-run behavior for testing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
