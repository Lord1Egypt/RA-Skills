## Description:

Generate a daily summary of your agent's activities, suitable for tracking progress and sharing updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3mr0i](https://clawhub.ai/user/t3mr0i)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to summarize daily agent activity, including commits, emails, messages, completed work, blockers, and next steps. It can also prepare a summary for optional Telegram sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily summaries may include private commits, emails, messages, blockers, or business details when shared through Telegram.

Mitigation: Review the generated summary before using --send, keep Telegram sending optional, and remove sensitive details before external sharing.

## Reference(s):

- [Clank Daily Summary on ClawHub](https://clawhub.ai/t3mr0i/skills/clank-daily-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown daily summary with command examples and optional Telegram delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default daily summaries, date-specific summaries, and user-invoked Telegram sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
