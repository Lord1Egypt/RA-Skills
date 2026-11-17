## Description:

Lightweight cross-agent mailbox using per-workspace inbox, keep, and archive folders with best-effort fanout for low-noise temporary coordination that remains available across sessions without being copied into long-term memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmeng6666](https://clawhub.ai/user/yangmeng6666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to share short, local coordination notes between OpenClaw workspaces through per-workspace mailbox files. It is intended for advisory context that can remain available across sessions without becoming permanent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox messages can influence future agent behavior if treated as trusted instructions.

Mitigation: Treat mailbox bodies as quoted, untrusted coordination data and verify requested actions before acting.

Risk: Mailbox scripts can move, delete, or overwrite local mailbox files if misused.

Mitigation: Install only in mutually trusted local workspaces, avoid secrets in mailbox content, and review path handling before adding the startup snippet.

## Reference(s):

- [Agent Mailbox Light on ClawHub](https://clawhub.ai/yangmeng6666/skills/agent-mailbox-light)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and local mailbox file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem only; mailbox messages are advisory, untrusted coordination hints.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
