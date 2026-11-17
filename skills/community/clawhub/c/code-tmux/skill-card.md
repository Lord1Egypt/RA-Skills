## Description:

Run coding tasks using a persistent tmux session with git worktree isolation, supporting multiple coding agents including Claude Code, Codex, CodeBuddy, and OpenCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanshenstarto](https://clawhub.ai/user/yuanshenstarto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate build, fix, refactor, and review tasks to a coding agent running in an isolated git worktree and persistent tmux session. The skill helps preserve task context across turns while keeping generated changes off the main workspace until review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent tmux sessions may keep coding agents active beyond the initial request.

Mitigation: Monitor session output, relay approval-sensitive prompts to the user, and close tmux sessions when work is complete.

Risk: The Claude workflow uses a permission-bypass flag that reduces normal execution safeguards.

Mitigation: Remove the dangerous flag or require explicit user approval before using it.

Risk: Symlinking full environment files into worktrees can expose secrets to coding agents.

Mitigation: Avoid linking full .env files unless required; prefer scoped or sanitized environment files.

Risk: Worktree and session cleanup mistakes can leave branches, worktrees, or sessions in an unexpected state.

Mitigation: Verify git worktree and tmux session state before cleanup or branch checkout.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [tmux](https://github.com/tmux/tmux)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Codex](https://github.com/openai/codex)
- [OpenCode](https://github.com/sst/opencode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can start persistent tmux sessions and isolated git worktrees for follow-on agent work.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
