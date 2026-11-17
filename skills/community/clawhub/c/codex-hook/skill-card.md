## Description:

Codex Hook helps agents dispatch, execute, monitor, intervene in, notify on, and optionally merge Codex-driven development tasks through shell workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lonelybeanz](https://clawhub.ai/user/lonelybeanz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to coordinate OpenClaw subtasks with Codex CLI execution, task tracking, progress reporting, and supervised intervention. It is suited for repository automation workflows where task execution, monitoring, notification, and optional pull request handling are intentionally enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously modify repositories and optionally merge pull requests with weak safety gates.

Mitigation: Use it only on intended repositories, disable or closely supervise auto-merge and auto-retry, and require human review plus CI checks before merging changes.

Risk: The skill can run Codex with broad approvals in writable workspaces.

Mitigation: Run tasks in isolated worktrees or sandboxes, keep prompts and workspace inputs trusted, and review generated changes before accepting them.

Risk: Task details and status can be sent to Telegram, Discord, or generic webhook services.

Mitigation: Configure only approved notification channels, avoid sending sensitive task content, and scope, rotate, and protect webhook and bot tokens.

Risk: GitHub credentials may be used for pull request creation, checks, and merge operations.

Mitigation: Use least-privileged GitHub credentials and prefer manual pull request handling for sensitive repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lonelybeanz/skills/codex-hook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output is terminal text, task logs, and JSON task registry data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local task registry files, worktrees, logs, notification messages, and pull request state when the scripts are executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
