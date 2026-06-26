## Description: <br>
Delegates coding, refactoring, PR review, and iterative file-exploration tasks to the Cursor Agent CLI through a PTY-capable bash tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rare](https://clawhub.ai/user/rare) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to spawn Cursor CLI agents for feature work, refactoring, code review, and scripted codebase analysis. It is intended for focused work directories, temporary clones, or git worktrees where the spawned agent can be monitored. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended Cursor CLI delegation can change code and publish repository updates without strong approval boundaries. <br>
Mitigation: Prefer plan or interactive modes, use isolated worktrees or temporary clones, avoid --yolo in sensitive repositories, and manually review diffs and generated text before any commit, push, PR creation, or GitHub comment. <br>
Risk: Interactive Cursor CLI sessions can hang or produce unreliable behavior when launched without PTY support. <br>
Mitigation: Run Cursor CLI commands with pty:true and monitor background sessions so the user can provide input or terminate stalled work. <br>


## Reference(s): <br>
- [Cursor CLI Agent on ClawHub](https://clawhub.ai/rare/cursor-cli-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON output from Cursor CLI print mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Cursor CLI agent binary and a PTY-capable bash tool; long-running tasks may be managed through background sessions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
