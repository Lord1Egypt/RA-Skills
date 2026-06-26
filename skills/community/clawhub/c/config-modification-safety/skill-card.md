## Description: <br>
Config Modification Safety helps OpenClaw users protect JSON configuration files by backing up valid changes, rolling back invalid edits, and checking gateway health for recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexduming](https://clawhub.ai/user/alexduming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and operate configuration safety checks that back up OpenClaw config files, roll back invalid JSON edits, and recover from gateway health failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent automation that monitors OpenClaw configs, restores backups, and restarts the gateway. <br>
Mitigation: Install only when that background behavior is intended, and review the installation steps and permissions before deployment. <br>
Risk: The release evidence reports incomplete install artifacts, including missing macOS plist and Windows installer/helper scripts. <br>
Mitigation: Require the missing platform artifacts to be supplied and reviewed before relying on the install workflow. <br>
Risk: The documented macOS uninstall command can remove the user's full crontab. <br>
Mitigation: Replace it with an uninstall step that removes only this skill's cron entry. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexduming/config-modification-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific install, rollback, logging, and uninstall commands for macOS and Windows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
