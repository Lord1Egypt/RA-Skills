## Description: <br>
Runs shell commands inside a dedicated tmux session named "claw", captures pane output, and blocks some potentially destructive commands until the user gives explicit approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlshiny](https://clawhub.ai/user/zlshiny) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run shell commands through an agent while keeping execution in a named tmux session and returning captured command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent local shell access, so allowed commands can affect local files, data, and the surrounding workspace. <br>
Mitigation: Install and run it only in a sandbox or trusted workspace with data and permissions appropriate for agent-driven command execution. <br>
Risk: The documented and implemented denylist is not a complete safety boundary for destructive or sensitive shell behavior. <br>
Mitigation: Require human review for risky command patterns and do not rely on the denylist as the sole approval or policy control. <br>
Risk: The tmux session boundary keeps execution in a named session but does not isolate the underlying host environment. <br>
Mitigation: Use operating-system, container, or workspace-level isolation when command execution must be constrained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zlshiny/claw-shell-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/zlshiny) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON object containing the submitted command, captured tmux pane output, or an error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands execute in the local tmux session named "claw"; blocked dangerous-command matches return an approval message instead of executing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
