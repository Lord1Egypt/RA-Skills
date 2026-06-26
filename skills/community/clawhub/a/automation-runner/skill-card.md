## Description: <br>
Executes approved shell commands, manages backups, and safely retrieves secrets from Bitwarden. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barnyp](https://clawhub.ai/user/barnyp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run approved OpenClaw system commands, retrieve runtime secrets through Bitwarden, manage backups, and verify command outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell execution can run unintended or overbroad commands if approval controls are weak. <br>
Mitigation: Use only with a real enforceable approval gate, a command allowlist, and a sandboxed scripts directory. <br>
Risk: Runtime secret retrieval and persistent command-output logging can expose credentials or sensitive output. <br>
Mitigation: Use narrow Bitwarden permissions and redact secrets and sensitive output, or disable logging when redaction cannot be guaranteed. <br>
Risk: Long-running process control can hide failed or stale backup tasks. <br>
Mitigation: Limit process management to approved tasks and verify command success before reporting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barnyp/automation-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approved command steps, runtime secret retrieval guidance, process status, and dated log notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
