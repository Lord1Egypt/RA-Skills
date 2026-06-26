## Description: <br>
Gateway Sentinel is an OpenClaw gateway watchdog that monitors gateway health, attempts escalating repairs, sends Telegram or Discord alerts, commits daily snapshots, and installs as a macOS launchd or Linux systemd service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run OpenClaw use this skill to keep a gateway process available, receive outage alerts, and apply controlled service repairs on macOS or Linux hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog runs persistently and can restart OpenClaw services and mutate the configured Git workspace. <br>
Mitigation: Review the configured workspace before installation, test the guardian in the foreground first, and monitor the generated service configuration before enabling always-on operation. <br>
Risk: Alert credentials can be loaded into service configuration and daily snapshots may commit files that are not ignored. <br>
Mitigation: Restrict permissions on ~/.openclaw/guardian.env, verify the generated service file for copied secrets, and confirm .gitignore excludes secret-bearing files before enabling snapshots. <br>
Risk: Optional rollback uses git reset behavior and can disrupt local workspace state if recovery has not been tested. <br>
Mitigation: Leave GUARDIAN_ENABLE_ROLLBACK=false unless recovery has been tested and backups or stash recovery procedures are in place. <br>


## Reference(s): <br>
- [Gateway Sentinel on ClawHub](https://clawhub.ai/zurbrick/gateway-sentinel) <br>
- [OpenClaw Guardian homepage](https://github.com/openclaw/openclaw-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires openclaw, git, and curl; supports macOS launchd and Linux systemd service setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
