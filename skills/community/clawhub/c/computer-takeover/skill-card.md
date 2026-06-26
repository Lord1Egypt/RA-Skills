## Description: <br>
Provides unattended remote control guidance for paired OpenClaw devices, including screen and camera capture, shell commands, file management, app control, notifications, input automation, location lookup, and process management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers with explicit authorization use this skill to administer paired devices: inspect device state, capture screen or camera output, run shell commands, manage files, control apps and processes, and automate input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad unattended access to paired devices, including screen, camera, files, commands, notifications, location, apps, and processes. <br>
Mitigation: Install only for devices you own or are explicitly authorized to manage, restrict reachable nodes, and keep pairings revocable. <br>
Risk: Shell commands, file changes, app installs, and process kills can modify or damage remote systems. <br>
Mitigation: Require confirmation for shell execution, file writes or deletion, installs, process termination, and other destructive or privileged actions. <br>
Risk: Screen capture, camera capture, notifications, and location access can expose sensitive personal or organizational information. <br>
Mitigation: Require explicit approval for capture or monitoring actions and log remote actions for later review. <br>


## Reference(s): <br>
- [Computer Takeover on ClawHub](https://clawhub.ai/fuzzyb33s/computer-takeover) <br>
- [Shell Command Reference by OS](references/shell-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool calls and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or actions that operate on paired remote devices; review the target node and command intent before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
