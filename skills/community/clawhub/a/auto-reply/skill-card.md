## Description:

auto-reply is an Instagram DM automation skill for monitoring, reading, replying to messages, setting up notification workflows, and rejecting common prompt-injection attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent check Instagram DMs, inspect unread conversations, prepare reply actions, and configure polling or watcher workflows. It is intended for workflows where the user intentionally grants access to a logged-in Instagram browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a logged-in Instagram browser session and use session cookies to read or send DMs.

Mitigation: Install and run it only in an account and browser session where that access is intentional, and stop browser debugging access when the workflow is not in use.

Risk: Watcher workflows can copy private DM previews to Discord when Discord-related environment variables are configured.

Mitigation: Do not set DISCORD_TOKEN or OWNER_DISCORD_ID unless forwarding DM previews is explicitly desired, and review the configured recipient before enabling watcher notifications.

Risk: The documented global npm dependency install broadens trust in globally available packages.

Mitigation: Prefer a reviewed local dependency install in a project directory and run the scripts from that controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/auto-reply)
- [Publisher profile](https://clawhub.ai/user/mupengi-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local DM state and alert files as part of watcher and auto-reply workflows.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
