## Description:

Call Claude Code as a non-interactive coding agent on a remote machine via OpenClaw Node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxuzzwz](https://clawhub.ai/user/xxuzzwz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate coding tasks to Claude Code running on a remote OpenClaw Node, especially when the gateway and coding environment are on separate machines or remote worktrees are preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes broad remote execution permissions, including full-permission command patterns.

Mitigation: Prefer read-only or narrowly allowlisted permissions, and reserve full-permission execution for trusted disposable environments.

Risk: Remote Node execution can affect systems outside the local gateway's direct control.

Mitigation: Install and use the skill only with remote Nodes that the user understands, controls, and can monitor.

Risk: The documented credential examples may encourage persistent shell-profile secrets or accidental secret disclosure.

Mitigation: Use a secret manager or scoped environment injection, and avoid printing API keys or storing long-lived secrets in shell startup files.

Risk: Untrusted task text placed into shell templates can change the executed command.

Mitigation: Avoid pasting untrusted task text into shell command templates; quote, review, and constrain commands before dispatch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxuzzwz/skills/claude-code-noninteractive-in-node)
- [Permission Mode Details](references/permissions.md)
- [Remote-Specific Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JSON command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes permission-mode recommendations, OpenClaw exec configuration, worktree setup, and remote troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
