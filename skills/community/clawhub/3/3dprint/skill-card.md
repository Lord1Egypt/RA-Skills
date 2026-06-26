## Description: <br>
Automate and control Flashforge Adventurer 5M 3D printers for status checks, print jobs, temperature monitoring, homing, file management, slicing, and camera snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickbmerrill-collab](https://clawhub.ai/user/nickbmerrill-collab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare, start, monitor, and manage Flashforge Adventurer 5M print jobs from an agent workflow. It is intended for authorized local printer control where users can verify configuration and physical safety before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a physical 3D printer, including actions that start, stop, pause, home, heat, or move hardware. <br>
Mitigation: Install and run it only when authorized to control the printer, and require explicit confirmation before any hardware-affecting action. <br>
Risk: The artifact documents fixed printer network details, a check code, and camera access that may expose a real device if reused unchanged. <br>
Mitigation: Replace the documented printer details with the user's own local configuration, rotate the check code if it is real, and secure the camera feed before use. <br>
Risk: The documented controller script is referenced but not included in the artifact evidence. <br>
Mitigation: Inspect the missing controller script and dependencies before running commands generated from this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickbmerrill-collab/3dprint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include printer control commands, local network endpoints, material settings, and operational guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
