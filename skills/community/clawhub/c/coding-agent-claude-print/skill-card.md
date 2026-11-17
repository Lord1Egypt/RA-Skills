## Description:

Delegates coding tasks to Codex, Claude Code, OpenCode, or Pi agents with guidance for working directories, background sessions, PTY usage, and Claude print-mode execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate coding, refactoring, PR review, and longer implementation tasks to supported agent CLIs while selecting the expected execution mode for each agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated agents may run with reduced or disabled safety controls.

Mitigation: Use the skill only in isolated repositories or disposable worktrees, and avoid --yolo or permission-bypass modes unless the operator explicitly accepts the risk.

Risk: Spawned agents may install dependencies, modify code, commit, push, or trigger host events.

Mitigation: Review the exact command before execution and inspect resulting file, dependency, git, and host-event changes before accepting or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielsinewe/skills/coding-agent-claude-print)
- [Publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one supported agent CLI: claude, codex, opencode, or pi.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
