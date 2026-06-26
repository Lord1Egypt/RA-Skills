## Description: <br>
Executes Windows shell commands locally on the OpenClaw gateway, returning output and errors for automation and system management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadikjarvis](https://clawhub.ai/user/sadikjarvis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run local Windows shell commands through an OpenClaw gateway and receive command output for automation or system management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run arbitrary local shell commands with broad host access. <br>
Mitigation: Install it only when local command execution is intended, limit use to trusted users and prompts, and run it inside a disposable VM or sandbox where practical. <br>
Risk: Commands may access private files, secrets, production credentials, or privileged host resources. <br>
Mitigation: Avoid installing or running it on machines that contain sensitive data or elevated privileges, and review command output before sharing it. <br>


## Reference(s): <br>
- [Cmd Executor on ClawHub](https://clawhub.ai/sadikjarvis/cmd-executor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell command output] <br>
**Output Format:** [Plain text containing stdout, stderr, or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs commands matching the documented Run command: prompt pattern and returns trimmed command output.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
