## Description:

Runs coding tasks through a persistent tmux session with git worktree isolation and support for Claude Code, Codex, OpenCode, CodeBuddy, or another interactive coding-agent CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanshenstarto](https://clawhub.ai/user/yuanshenstarto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate build, fix, refactor, and review tasks to a selected coding-agent CLI while preserving an isolated git worktree and persistent tmux conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow symlinks project .env files into task worktrees, which can expose secrets to the launched coding agent.

Mitigation: Use redacted or non-production environment files, remove secret symlinks when they are not needed, and avoid running the skill in workspaces that contain production credentials.

Risk: The Claude Code launch command uses a permission-bypass mode that can allow broad unchecked file and command access.

Mitigation: Remove the permission-bypass flag and run the selected agent with explicit approval prompts or a restricted sandbox.

Risk: Remembered custom CLI commands may execute unexpected tools in future tasks.

Mitigation: Store only trusted coding-agent commands, review memory entries before reuse, and clear or update the preference when switching workspaces.

Risk: Installing through an unpinned latest package can change behavior between installs.

Mitigation: Pin the installer or release version and review the skill files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanshenstarto/skills/claude-code-tmux)
- [Troubleshooting](references/troubleshooting.md)
- [tmux](https://github.com/tmux/tmux)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Codex](https://github.com/openai/codex)
- [OpenCode](https://github.com/sst/opencode)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for tmux sessions, git worktrees, CLI launch commands, and user relay steps.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
