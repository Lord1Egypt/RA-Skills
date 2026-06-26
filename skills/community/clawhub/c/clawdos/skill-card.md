## Description: <br>
Windows automation via Clawdos API: screen capture, mouse/keyboard input, window management, file-system operations, and shell command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danzig233](https://clawhub.ai/user/danzig233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an OpenClaw agent to an authorized Windows host for remote inspection, GUI automation, sandboxed file work, and shell-based troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent remote control of a configured Windows host. <br>
Mitigation: Install only for authorized hosts, bind the Clawdos service to trusted interfaces, protect and rotate the API key, and run the server with least privilege. <br>
Risk: Shell execution, file deletion, moves, uploads, and downloads can change host or workspace state. <br>
Mitigation: Review commands and file operations before allowing them, confirm destructive paths, and keep filesystem sandbox configuration narrow. <br>
Risk: Screen capture and window inspection can expose sensitive visible information. <br>
Mitigation: Avoid captures when passwords, tokens, personal data, or confidential content are visible on the Windows host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danzig233/clawdos) <br>
- [Publisher profile](https://clawhub.ai/user/danzig233) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots or binary file transfers to local paths when requested.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and OpenClaw frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
