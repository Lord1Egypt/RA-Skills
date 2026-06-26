## Description: <br>
Installs OpenClaw Gateway as a Windows scheduled task so it starts on boot and restarts after crashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suncxw-creator](https://clawhub.ai/user/suncxw-creator) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators on Windows use this skill to keep OpenClaw Gateway running unattended, restart it after crashes, and manage it with install, start, stop, restart, and status commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup creates a persistent Windows scheduled task that starts OpenClaw Gateway on boot and restarts it after exits. <br>
Mitigation: Install it only when you want always-on background operation, review the scheduled task after installation, and use the documented stop or status commands when you no longer want it running. <br>
Risk: Installation requires administrator privileges. <br>
Mitigation: Run the install command only from a trusted OpenClaw environment and confirm the task name and behavior before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suncxw-creator/gateway-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and a command table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents Windows Scheduled Task management for OpenClaw Gateway; installation requires administrator privileges.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
