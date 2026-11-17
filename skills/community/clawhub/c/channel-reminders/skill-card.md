## Description:

Creates scheduled reminders through cron jobs and delivers them to Telegram, including reminders routed through a main agent for multi-agent setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex3alex](https://clawhub.ai/user/alex3alex)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure scheduled reminders that deliver Telegram notifications at a specific time, on a cron schedule, or at an interval. It also documents how non-main agents can route reminders through a main agent when direct delivery is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies persistent agent behavior and can send Telegram messages through configured bot accounts from future scheduled events without validation.

Mitigation: Install only after accepting that behavior, and add explicit recipient and account allowlists plus event validation before use.

Risk: Reminder setup examples include a concrete Chat ID and recommend saving the working delivery approach, which can expose recipient identifiers if copied into general memory.

Mitigation: Replace hardcoded Chat IDs, avoid storing Chat IDs in general memory, and keep recipient identifiers in protected configuration where possible.

Risk: Suppressing all output after message delivery can reduce auditability for scheduled sends.

Mitigation: Keep an auditable record of reminder creation and delivery decisions instead of suppressing all operational output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex3alex/skills/channel-reminders)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reminder schedule patterns, Telegram delivery setup, post-install testing steps, and reminder management commands.]

## Skill Version(s):

1.3.0 (source: server-resolved release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
