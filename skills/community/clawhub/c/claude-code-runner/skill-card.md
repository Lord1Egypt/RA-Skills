## Description: <br>
Execute programming tasks via Claude Code using PTY-based invocation. Handles non-TTY environments, auto-responds to prompts, and manages file synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhl09120](https://clawhub.ai/user/lhl09120) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to run Claude Code tasks in non-interactive Unix-like environments for code review, refactoring, feature work, and bug fixing while capturing output and synchronizing successful changes back to the project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-approve Claude Code confirmation prompts. <br>
Mitigation: Run it only in a disposable container or throwaway version-controlled copy until auto-approval is explicitly controlled. <br>
Risk: The skill can write changes back to the target project. <br>
Mitigation: Use a dedicated copy of the repository and review diffs before keeping or deploying changes. <br>
Risk: The skill is vulnerable to unintended shell command execution. <br>
Mitigation: Avoid untrusted prompts or unusual project paths, use an unprivileged dedicated user, and avoid sudo or root execution. <br>


## Reference(s): <br>
- [Claude Code Runner on ClawHub](https://clawhub.ai/lhl09120/claude-code-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands] <br>
**Output Format:** [Plain text command output with project file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write changes back to the target project when the Claude Code process exits successfully.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
