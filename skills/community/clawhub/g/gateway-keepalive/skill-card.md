## Description: <br>
Helps an agent install, inspect, and manage a macOS keepalive setup that keeps OpenClaw Gateway running with LaunchAgents, health checks, automatic recovery, logging, and optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooey](https://clawhub.ai/user/jooey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run OpenClaw Gateway on macOS use this skill to install persistent LaunchAgents, check gateway health, recover from repeated failures, and review keepalive logs and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent macOS LaunchAgents and can restart OpenClaw Gateway automatically. <br>
Mitigation: Review the install and recovery scripts before running them, confirm they target the intended macOS user account, and inspect the generated LaunchAgent plist files before loading them. <br>
Risk: The recovery script reads ~/.openclaw/config/keepalive.conf as shell configuration and may use Telegram notification credentials. <br>
Mitigation: Keep the configuration file writable only by the local user, do not place untrusted content in it, and configure Telegram credentials only when external notifications are required. <br>
Risk: Automatic recovery can restore OpenClaw configuration from a golden backup. <br>
Mitigation: Maintain the golden backup only from a verified working configuration and review recovery history after major Gateway configuration changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jooey/gateway-keepalive) <br>
- [Gateway Keepalive Setup Guide](docs/gateway-keepalive-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets macOS OpenClaw Gateway environments and references local user configuration, logs, LaunchAgents, and backups.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact files report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
