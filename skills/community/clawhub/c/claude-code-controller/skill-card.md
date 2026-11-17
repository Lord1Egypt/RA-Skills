## Description:

专门控制 Claude Code 的技能。提供简化的命令接口，支持快速任务、长时间任务、并行任务和进度跟踪。

This skill is ready for commercial/non-commercial use.

## Publisher:

[steven-chen13](https://clawhub.ai/user/steven-chen13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to run Claude Code for quick tasks, longer background work, parallel worktree tasks, code review, refactoring, and progress tracking from a project or temporary workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends bypassing Claude Code permission checks for code-changing tasks.

Mitigation: Use it only in isolated project directories or disposable worktrees, avoid bypassing permission checks for routine work, and review commands before execution.

Risk: Prompts, logs, or task descriptions could expose secrets or sensitive project details to Claude Code.

Mitigation: Do not paste secrets or sensitive logs into prompts; redact sensitive data before using the command templates.

Risk: The recursive chmod troubleshooting guidance could change permissions more broadly than intended.

Mitigation: Run permission changes only after identifying the exact file or directory that needs access changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steven-chen13/skills/claude-code-controller)
- [Publisher profile](https://clawhub.ai/user/steven-chen13)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Claude Code CLI binary named claude.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
