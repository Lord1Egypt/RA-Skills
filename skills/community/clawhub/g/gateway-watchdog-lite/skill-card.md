## Description: <br>
Installs a macOS or Linux service that probes the OpenClaw gateway every 2 minutes and auto-recovers it on failure, sending Telegram alerts when configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[judas-oc](https://clawhub.ai/user/judas-oc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install a user-level watchdog for an OpenClaw gateway on macOS or Linux. It monitors local gateway health, attempts recovery after failed probes, and can send Telegram status alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a background user service that keeps running and can restart the local OpenClaw gateway. <br>
Mitigation: Install it only when continuous watchdog recovery is desired, verify WORKSPACE_PATH and OC_PORT before installation, and use the documented launchctl or systemctl uninstall commands when it is no longer needed. <br>
Risk: Telegram alerts may send gateway status messages when TELEGRAM_ID is configured. <br>
Mitigation: Set TELEGRAM_ID to an empty string to disable Telegram alerts. <br>
Risk: The Lite release does not include crash loop detection or auto-mitigation. <br>
Mitigation: Review the watchdog logs after recoveries and handle repeated gateway failures manually or use a version that includes crash loop mitigation. <br>


## Reference(s): <br>
- [Gateway Watchdog Lite on ClawHub](https://clawhub.ai/judas-oc/gateway-watchdog-lite) <br>
- [Gateway Watchdog Gotchas](references/gotchas.md) <br>
- [ConfusedUser.com](https://confuseduser.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command blocks and environment-variable instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and operations guidance for a background launchd or systemd watchdog service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
