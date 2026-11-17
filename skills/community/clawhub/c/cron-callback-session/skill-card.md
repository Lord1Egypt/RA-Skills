## Description:

Enables cron jobs, external processes, or another OpenClaw/QClaw session to inject a message into a target session with `sessions_send` so the agent can continue work with the existing context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onesfuture](https://clawhub.ai/user/onesfuture)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to route cron job results, external process notifications, or cross-session updates back into a specific OpenClaw/QClaw conversation. It is intended for workflows where a target session should be awakened to continue work with its existing context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables session callback and message injection into existing sessions.

Mitigation: Install only when callback routing is deliberately needed, limit targets to explicit sessions, and verify the target session before sending.

Risk: Broader session routing settings can allow more sessions to send messages to one another.

Mitigation: Prefer the narrowest workable visibility, avoid visibility=all and wildcard cross-agent rules, and restore the default routing setting after use.

Risk: Gateway restarts or forced process stops can interrupt active sessions, cron jobs, or other work.

Mitigation: Restart only during a maintenance window, back up configuration first, and verify the gateway is healthy after restart.

Risk: A timeout while the target session is busy can be mistaken for failed delivery, causing duplicate injected messages if retried.

Mitigation: Confirm delivery in the target session before retrying and account for queued delivery delays.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onesfuture/skills/cron-callback-session)
- [WorkBuddy session callback skill](https://github.com/onesfuture/workbuddy-skill-session-callback)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell, PowerShell, and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checks, configuration changes, restart guidance, cron job design, and callback verification steps.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter says 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
