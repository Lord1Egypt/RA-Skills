## Description: <br>
Delegates coding work to Codex, Claude Code, OpenCode, or Pi agents through bash commands, background sessions, and focused build or review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate larger coding, refactoring, app-building, and PR-review tasks to coding-agent CLIs while monitoring their background sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage broad auto-approved coding-agent execution with host or remote side effects. <br>
Mitigation: Use sandboxed or approval-gated modes, avoid yolo and permission-bypass modes except in disposable worktrees, and review commits, pushes, PR creation, comments, and events before allowing them. <br>
Risk: Background coding-agent sessions may continue making project changes after launch. <br>
Mitigation: Monitor session output and status, keep secrets out of the working directory, and terminate sessions that drift from the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/ai-coding-delegate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch and monitor background coding-agent sessions when the host environment provides the required CLI tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
