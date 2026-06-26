## Description: <br>
ClawShorts helps an agent manage a Fire TV YouTube Shorts limiter that tracks daily Shorts watch time and closes YouTube when the configured limit is reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindulasai](https://clawhub.ai/user/cindulasai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up, monitor, and configure a local Fire TV YouTube Shorts limiter through ADB, including status checks, resets, device management, and daemon control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ADB to control Fire TV devices on the local network. <br>
Mitigation: Use it only on a trusted, password-protected home network and disable ADB debugging when the limiter is not needed. <br>
Risk: The background daemon can close YouTube automatically when the daily limit is reached. <br>
Mitigation: Review the configured devices and daily limits before enabling the daemon, and use the documented stop or reset commands when enforcement is not desired. <br>
Risk: Local logs or UI dump files may contain sensitive screen or usage details. <br>
Mitigation: Periodically review or delete local files under ~/.clawshorts and /tmp when screen contents or usage history may be sensitive. <br>


## Reference(s): <br>
- [ClawShorts ClawHub Release](https://clawhub.ai/cindulasai/clawshorts) <br>
- [README](artifact/README.md) <br>
- [Security Audit Report](artifact/SECURITY_AUDIT.md) <br>
- [Per-Device Config and Auto-Detection Spec](artifact/SPEC.md) <br>
- [Troubleshooting Guide](artifact/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell commands and status or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that interact with local ADB, SQLite configuration, and a user-level background daemon.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
