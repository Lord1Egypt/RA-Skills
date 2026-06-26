## Description: <br>
Blocks YouTube Shorts on Fire TV by monitoring Shorts watch time, enforcing a daily limit, and closing YouTube when the limit is reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindulasai](https://clawhub.ai/user/cindulasai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Household users and administrators use this skill through an agent to set up, check, reset, start, stop, and troubleshoot a local Fire TV YouTube Shorts limiter. The skill is intended for Fire TV or Fire Stick devices on a trusted local network with ADB debugging enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a background local daemon that controls YouTube on configured Fire TV devices over ADB. <br>
Mitigation: Install it only for intended Fire TV devices on a trusted home network, and keep ADB debugging disabled when this control is not needed. <br>
Risk: The auto-start service can persist on the host after setup. <br>
Mitigation: Review the launchd or systemd service created during installation, and use the uninstall command when the limiter should no longer run automatically. <br>
Risk: Logs and status output can include device IPs and viewing-status details. <br>
Mitigation: Avoid sharing logs publicly and redact local network addresses or usage details before sending troubleshooting information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cindulasai/clawshorts-pkg) <br>
- [Android Debug Bridge documentation](https://developer.android.com/tools/adb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local device IPs, daemon status, usage counters, and log paths when needed for setup or troubleshooting.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
