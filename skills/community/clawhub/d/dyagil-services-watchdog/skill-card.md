## Description: <br>
Helps an agent set up a user-systemd watchdog that monitors and restarts long-running Node.js services across shell exits, SSH disconnects, runtime restarts, and server reboots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to stabilize always-on Node.js services, customize watchdog checks, and install user-systemd timer-based recovery for service restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included script is personalized and can send Telegram status messages to a hard-coded chat using a local bot token. <br>
Mitigation: Remove the Telegram notification block or explicitly configure the bot token source and chat ID before enabling the watchdog. <br>
Risk: The watchdog restarts hard-coded local projects and loads service .env files into new systemd scopes. <br>
Mitigation: Replace all service paths, process checks, unit names, and startup commands, then inspect the environment files and credentials each service will load. <br>
Risk: The install flow references systemd unit files that are not included in the artifact. <br>
Mitigation: Create and review the user service and timer unit files yourself before running systemctl enable or start commands. <br>
Risk: Enabling a user timer and loginctl linger can keep services running after logout or reboot. <br>
Mitigation: Confirm that persistent background execution is intended and document how to disable the timer and loginctl linger for the target user. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands, configuration steps, and shell script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and customization guidance for systemd user timers and a service watchdog shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
