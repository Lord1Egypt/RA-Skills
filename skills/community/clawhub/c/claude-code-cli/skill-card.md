## Description: <br>
Delegate coding tasks to Claude Code CLI via background process for feature work, PR review, refactoring, and iterative coding that needs file exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtelyPham](https://clawhub.ai/user/AtelyPham) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to delegate scoped coding, refactoring, PR review, and automation tasks to Claude Code CLI from OpenClaw. It supports interactive PTY sessions, headless structured-output runs, session resumption, and background task monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegating coding work to Claude Code can run commands and edit files in the selected workspace. <br>
Mitigation: Use clean git worktrees or temporary clones, avoid sensitive directories and ~/.openclaw, and review all diffs before pushing or opening PRs. <br>
Risk: Unattended or background Claude Code sessions can consume budget, stall on permissions, or continue longer than intended. <br>
Mitigation: Prefer plan mode for review, set budgets and timeouts for unattended runs, monitor background sessions, and avoid permission-bypass modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtelyPham/claude-code-cli) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or stream-json CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the claude binary; guidance covers PTY, headless pipe mode, permission modes, budgets, sessions, and background monitoring.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
