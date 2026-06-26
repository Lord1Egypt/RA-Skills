## Description: <br>
Manage and monitor multiple OpenClaw agents simultaneously, including status checks, messaging, logs, pausing, resuming, and workspace management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate OpenClaw agent groups, inspect status and logs, send broadcasts, pause or resume agents, run health checks, and manage local agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove local workspaces. <br>
Mitigation: Use only with trusted operators and non-critical workspaces until removal actions require validation and explicit confirmation. <br>
Risk: Shell commands are built from user-controlled inputs. <br>
Mitigation: Replace shell command construction with safer APIs where possible, or add strict input validation and quoting before trusted deployment. <br>
Risk: The documented heartbeat behavior may run ongoing monitoring without clear packaging or controls. <br>
Mitigation: Make heartbeat behavior opt-in with clear controls, or remove it from documentation until it is packaged and governed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lunaviva211-sketch/colmena-manager) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text, command results, and agent messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local workspace operations and OpenClaw agent-management commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
