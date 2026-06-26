## Description: <br>
Runs shell commands inside a dedicated tmux session named claw, captures command output, and returns it to the agent with basic checks for destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaginelogo](https://clawhub.ai/user/imaginelogo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run local shell commands in a persistent tmux session and retrieve recent command output for follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent local shell access, and the server security summary says its safeguards are too weak for that level of control. <br>
Mitigation: Install only when local shell access is intentional, use a disposable or sandboxed environment, and approve commands carefully. <br>
Risk: Command output in the tmux session may expose secrets or sensitive local context. <br>
Mitigation: Avoid displaying secrets in the tmux session and inspect or kill the claw tmux session when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaginelogo/claw-shell) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON object containing the command, captured output, or a safety error] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are sent to a tmux session named claw; recent pane output is captured and returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
