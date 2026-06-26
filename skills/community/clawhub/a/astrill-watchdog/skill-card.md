## Description: <br>
Monitors Astrill StealthVPN on Ubuntu and restarts Astrill when the tun0 tunnel or ping check indicates the VPN is down. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LittleJakub](https://clawhub.ai/user/LittleJakub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Linux desktop users and agents managing Ubuntu Astrill installations use this skill to install and operate a user-level watchdog that monitors VPN health, writes local diagnostics, and restarts Astrill when connectivity drops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog installs a background systemd user service that starts automatically on login. <br>
Mitigation: Review the setup behavior before installation and disable the systemd user service when automatic monitoring is no longer wanted. <br>
Risk: The watchdog can automatically kill and relaunch Astrill when connectivity checks fail. <br>
Mitigation: Use it only when automatic Astrill recovery is desired, and test the status or one-shot commands before relying on the continuous loop. <br>
Risk: The default health check pings 8.8.8.8 and writes local VPN diagnostic logs. <br>
Mitigation: Review the ping host, timing settings, and log location before use, then adjust the configuration block if those defaults do not fit the environment. <br>


## Reference(s): <br>
- [ClawHub release: Astrill Watchdog](https://clawhub.ai/LittleJakub/astrill-watchdog) <br>
- [Artifact documentation](artifact/SKILL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Bash commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Ubuntu user-service setup, watchdog operation, status, logging, and diagnostic guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
