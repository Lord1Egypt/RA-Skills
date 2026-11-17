## Description:

Monitors Astrill StealthVPN on Ubuntu and helps automatically restart Astrill when the VPN tunnel drops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlejakub](https://clawhub.ai/user/littlejakub)

### License/Terms of Use:


## Use Case:

Linux users and administrators who run Astrill VPN on Ubuntu use this skill to install and operate a user-level watchdog that checks tunnel and ping health, restarts Astrill when StealthVPN drops, and reports status and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog runs as a background user service that can kill and relaunch Astrill when connectivity checks fail.

Mitigation: Review the start, stop, and restart behavior before enabling it, and use the documented stop command or systemd user controls when it should no longer run at login.

Risk: The PID-matching behavior has a weakness that could stop an unrelated same-user process in edge cases.

Mitigation: Review the process-matching pattern before installation and monitor status and logs after enabling the service.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No structured API output; generated guidance is intended for Ubuntu desktop environments with Astrill installed.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
