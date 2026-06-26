## Description: <br>
Cloud Mount helps users configure rclone-based mounts so cloud storage such as OneDrive or Google Drive can be used like a local folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liqiuyue9597](https://clawhub.ai/user/liqiuyue9597) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, server operators, and individual users use this skill to mount personal or team cloud storage, check mount status, and configure optional user-level autostart for recurring access or backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires rclone credentials for the selected cloud account. <br>
Mitigation: Use a dedicated or least-privilege cloud folder or account, and protect rclone and cloud-mount configuration files with restrictive file permissions. <br>
Risk: Autostart setup can make mounts persistent across sessions. <br>
Mitigation: Prefer the documented user-level systemd service and avoid running autostart setup with sudo unless a system-level service is intentionally required. <br>
Risk: Backup examples that use rsync with delete behavior can remove files from the destination if misconfigured. <br>
Mitigation: Test backup commands with --dry-run before using destructive sync options. <br>


## Reference(s): <br>
- [Cloud Mount on ClawHub](https://clawhub.ai/liqiuyue9597/cloud-mount) <br>
- [rclone documentation](https://rclone.org/docs/) <br>
- [rclone downloads](https://rclone.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands and scripts for rclone mounting, status checks, and systemd user autostart setup.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
