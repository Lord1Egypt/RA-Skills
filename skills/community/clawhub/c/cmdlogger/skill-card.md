## Description: <br>
Execute commands with real-time console output while logging all stdin, stdout, and stderr to a customizable log file for monitoring and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run commands while preserving complete stdin, stdout, and stderr logs for builds, long-running scripts, debugging sessions, CI/CD runs, and execution tracing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The logger can record everything typed into arbitrary commands, including passwords, tokens, SSH prompts, sudo input, and production credentials. <br>
Mitigation: Use it only when full command I/O logging is required, avoid interactive commands that request secrets, and prefer a redacting logger for sensitive workflows. <br>
Risk: Command logs may contain sensitive operational data and can grow large during verbose or long-running commands. <br>
Mitigation: Choose a private log path with restricted permissions, ensure sufficient disk space, and rotate or delete logs after review. <br>
Risk: The release evidence flags the skill as suspicious because its legitimate logging purpose has privacy and credential-exposure risks. <br>
Mitigation: Verify the actual cmdlogger binary before use and review whether full I/O capture is appropriate for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/cmdlogger) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples and logging guidance; command logs can contain full stdin, stdout, and stderr.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
