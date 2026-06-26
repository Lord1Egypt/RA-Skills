## Description: <br>
Guides an agent to delegate complex coding tasks to Codex, Claude Code, OpenCode, or Pi through PTY-backed bash sessions and background process monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to launch and supervise coding agents for feature work, refactoring, PR review, and other multi-step codebase tasks. It is intended for complex delegation workflows, not simple edits or code reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: No-approval or unsandboxed agent modes can make broad workspace or host changes. <br>
Mitigation: Use temporary clones or worktrees, avoid --yolo unless the workspace is disposable, and inspect diffs before commits. <br>
Risk: Background coding-agent sessions can continue acting after launch without enough user checkpoints. <br>
Mitigation: Monitor session logs and status, terminate stale runs, and require explicit approval before pushes, PR creation, package installs, or GitHub comments. <br>
Risk: Host notification commands may trigger external side effects when appended to long-running prompts. <br>
Mitigation: Require explicit user approval before host notification commands and keep completion messages limited to task status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/coding-agent-cp3d) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bash-capable environment with PTY support and the selected coding agent CLI installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
