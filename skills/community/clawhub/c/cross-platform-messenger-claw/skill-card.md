## Description: <br>
Coordinates cross-platform message delivery through OpenClaw CLI commands for text, media, broadcasts, scheduled notifications, and alert-driven sends across supported messaging services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare OpenClaw message commands and scripts for direct, bulk, scheduled, or condition-triggered notifications across chat and messaging platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bulk-send script can accidentally turn message, media, or recipient text into local shell commands. <br>
Mitigation: Prefer direct OpenClaw message commands or dry-run mode, and avoid scripts/notify.sh with untrusted message text, media paths, or target lists until the script is reviewed. <br>
Risk: Messaging workflows can send live content to unintended recipients, channels, or scheduled jobs. <br>
Mitigation: Confirm exact recipients, channels, content, attachments, and schedules before allowing live sends. <br>


## Reference(s): <br>
- [Cross-platform channel reference](references/channels.md) <br>
- [ClawHub release page](https://clawhub.ai/tujinsama/cross-platform-messenger-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw message and cron commands; live sends should be preceded by recipient, channel, content, and schedule confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
