## Description:

Claude-native multi-agent swarm orchestration for parallel coding with git worktrees, tmux tracking, endorsement gates, auto-review chains, integration merging, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkbag](https://clawhub.ai/user/linkbag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to split parallel coding work across multiple Claude Code agents, track each task in an isolated worktree, review branch output, and coordinate integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended agents can run with broad repository authority, including permission bypass, commits, pushes, and default main-branch integration.

Mitigation: Use a disposable or tightly sandboxed repository with test-scoped credentials, disable auto-merge unless explicitly needed, and review every generated branch before pushing or merging.

Risk: Notification and automation scripts can run long-lived watchers and send status externally when configured.

Mitigation: Keep notifications disabled unless required, scope webhook or Telegram credentials narrowly, and verify the configured destination before running batch workflows.

Risk: Cleanup and integration scripts can alter worktrees, branches, and remote repository state.

Mitigation: Run cleanup and integration commands only in non-production repositories or after confirming branch names, remotes, and pending changes.

## Reference(s):

- [Claude Swarm on ClawHub](https://clawhub.ai/linkbag/skills/claude-swarm)
- [linkbag publisher profile](https://clawhub.ai/user/linkbag)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON task definitions, shell script execution, git branches, pull requests, and notification messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository changes through delegated Claude Code agents and may create worktrees, branches, commits, pull requests, logs, and notifications.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
