## Description: <br>
Coding Agent Common helps agents delegate coding tasks to Codex, Claude Code, OpenCode, and similar tools for feature development, refactoring, bug fixing, code review, and iterative development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whiskeyforsun](https://clawhub.ai/user/whiskeyforsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding work to local AI coding agents. It supports feature implementation, refactoring, bug fixing, code review, background task monitoring, and iterative development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes permission-bypass and auto-approval modes that can modify real projects with limited user gating. <br>
Mitigation: Use it only in trusted, backed-up repositories or temporary worktrees; prefer constrained approval modes and review diffs before pushing. <br>
Risk: Background coding-agent sessions can continue running and changing files after launch. <br>
Mitigation: Monitor active sessions and logs, stop unneeded sessions, and confirm completion before relying on or publishing the results. <br>
Risk: Git and PR workflows can publish changes using the active remote and account. <br>
Mitigation: Confirm the current worktree, git remote, branch, and authenticated account before running push or PR commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whiskeyforsun/coding-agent-common) <br>
- [Claude Code command reference](references/claude-code-commands.md) <br>
- [Codex command reference](references/codex-commands.md) <br>
- [Prompt templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include background task monitoring steps, worktree workflows, and PR command guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
