## Description: <br>
Coding Agent Local helps an agent delegate project coding tasks to local coding-agent CLIs such as Codex, Claude Code, OpenCode, or Pi through Bash workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to launch local coding agents for feature work, pull request review, large refactors, and iterative project changes while keeping the agent focused on an explicit workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes launching high-authority local coding agents that may change files, run commands, publish code, or operate with reduced approval friction. <br>
Mitigation: Use sandboxed or approval-gated modes for important repositories, prefer temporary clones or git worktrees, avoid permission-bypass modes unless intentional, and review all changes before commit, push, or pull request creation. <br>
Risk: Completion notifications or delegated prompts can expose secrets, sensitive source details, or repository context to tools and logs. <br>
Mitigation: Keep notifications brief, omit secrets and sensitive code details from prompts and status messages, and run agents only in workspaces appropriate for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/coding-agent-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one supported local agent binary: claude, codex, opencode, or pi.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
