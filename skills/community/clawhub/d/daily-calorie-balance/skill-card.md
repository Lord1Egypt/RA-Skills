## Description:

Combines food intake records with Garmin calorie expenditure data to summarize daily calorie balance and practical health guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvzaiyi-afk](https://clawhub.ai/user/lvzaiyi-afk)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare food intake with Garmin calorie expenditure for today, yesterday, or a specified date, and to receive a daily summary on a schedule when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic mode can send sensitive diet and Garmin health summaries to a fixed QQBot recipient.

Mitigation: Do not enable the cron job or use --auto unless the recipient is user-owned and the user has explicitly opted in.

Risk: Daily calorie summaries may expose personal health and diet patterns outside the local workspace.

Mitigation: Preview output locally first, then configure a user-controlled destination before external delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvzaiyi-afk/skills/daily-calorie-balance)
- [Publisher profile](https://clawhub.ai/user/lvzaiyi-afk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style daily calorie summary with optional shell commands for manual runs and cron setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send the generated summary to a configured chat channel when run in automatic mode.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
