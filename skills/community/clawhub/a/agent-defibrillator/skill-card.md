## Description: <br>
Watchdog that monitors an OpenClaw or similar AI agent gateway on macOS and restarts it when it crashes or runs a stale version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hazy2go](https://clawhub.ai/user/hazy2go) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators who run OpenClaw or similar launchd-managed AI agent gateways use this skill to install and configure a watchdog that checks gateway health, restarts failed or stale processes, and provides optional Discord notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can fetch unpinned remote code before registering a persistent launchd service. <br>
Mitigation: Review the files first, install from a pinned commit or trusted release, and use the bundled local defibrillator.sh or verify a checksum before launchd runs it. <br>
Risk: The watchdog is designed to persist on macOS and restart the configured gateway automatically. <br>
Mitigation: Install only when persistent automatic restart behavior is intended, verify the launchd label and interval, and use the documented launchctl and file-removal commands to stop or uninstall it. <br>
Risk: Restart recovery can terminate orphaned gateway processes. <br>
Mitigation: Confirm the gateway label and process name match the intended OpenClaw service before deployment, then monitor watchdog logs after installation. <br>


## Reference(s): <br>
- [Agent Defibrillator ClawHub page](https://clawhub.ai/hazy2go/agent-defibrillator) <br>
- [Agent Defibrillator README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, verification, configuration, troubleshooting, and uninstall guidance for a macOS launchd watchdog.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
