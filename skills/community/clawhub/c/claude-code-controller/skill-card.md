## Description: <br>
专门控制 Claude Code 的技能。提供简化的命令接口，支持快速任务、长时间任务、并行任务和进度跟踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steven-chen13](https://clawhub.ai/user/steven-chen13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to launch and manage Claude Code sessions for quick tasks, longer background work, parallel worktree-based tasks, code review, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages launching Claude Code with permission checks bypassed, including background and parallel sessions. <br>
Mitigation: Review carefully before installing, prefer normal permission modes, explicitly approve background or parallel runs, and monitor or stop sessions when complete. <br>
Risk: Running agent sessions against sensitive repositories or broad directories can expose or modify files outside the intended task scope. <br>
Mitigation: Use the skill only in intentional project or temporary directories and avoid sensitive repositories or directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steven-chen13/claude-code-controller) <br>
- [Publisher profile](https://clawhub.ai/user/steven-chen13) <br>
- [Claude Code CLI package](https://www.npmjs.com/package/@anthropic-ai/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Claude Code CLI binary named claude.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
