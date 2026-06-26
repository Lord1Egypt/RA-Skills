## Description: <br>
Monitors email in real time via IMAP IDLE and triggers the OpenClaw agent to notify users through active channels like Telegram or Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canihojr](https://clawhub.ai/user/canihojr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, and manage a persistent IMAP watcher that pushes new-email events to an active agent channel. It is intended for mailbox notification workflows, connection testing, Telegram command registration, service troubleshooting, and controlled email reply behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a boot-starting service that continuously monitors the configured mailbox. <br>
Mitigation: Install only when persistent mailbox monitoring is intended, review the service configuration, and uninstall the service when it is no longer needed. <br>
Risk: The service configuration can contain the mailbox password and an OpenClaw gateway token. <br>
Mitigation: Use an app-specific email password, keep /opt/imap-watcher/watcher.conf restricted, and review the stored values after installation or reconfiguration. <br>
Risk: Auto-reply can expose that the system is active or send unintended replies. <br>
Mitigation: Keep auto-reply set to false or ask unless the user explicitly accepts the behavior for the mailbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canihojr/bee-push-email-skill) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide installation of a persistent systemd service and generation of local service configuration.] <br>

## Skill Version(s): <br>
1.5.3 (source: server evidence release metadata, artifact _meta.json, and changelog released 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
