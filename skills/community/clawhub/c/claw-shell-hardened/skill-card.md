## Description: <br>
Run shell commands inside a dedicated tmux session named `claw` and return output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run shell commands in a dedicated `claw` tmux session while capturing recent pane output. It is intended for local command execution workflows that require explicit session isolation and basic command safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local shell-command capability. <br>
Mitigation: Install only in a disposable or tightly sandboxed workspace and keep secrets out of the environment. <br>
Risk: The built-in dangerous-command blocklist is not a complete safety boundary. <br>
Mitigation: Review commands before execution and do not rely on the blocklist alone for destructive commands or outbound data transfer. <br>
Risk: Captured command output or local file contents could be sent to external endpoints if an agent is allowed to run network-transmitting commands. <br>
Mitigation: Block or manually review commands that pipe, redirect, or upload local data to external services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/claw-shell-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/claw-shell) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [JSON object containing the command and captured tmux pane output, or an error object for blocked commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local tmux environment and runs commands in the `claw` session.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
