## Description: <br>
Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding implementation, review, refactoring, and exploratory development tasks to background coding-agent CLIs while monitoring and managing their sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes high-autonomy coding agents that can modify repositories, install dependencies, push branches, create PRs, or post GitHub comments. <br>
Mitigation: Use temp clones or git worktrees, avoid directories containing secrets, monitor background logs, and require explicit approval before enabling broad autonomy or external side effects. <br>
Risk: Bypass or full-auto modes can reduce review gates around generated code and shell commands. <br>
Mitigation: Review proposed changes and command output before merging, pushing, publishing, or running commands outside an isolated workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/coding-delegate-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include background-session management steps, workspace isolation guidance, and tool-specific execution modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
