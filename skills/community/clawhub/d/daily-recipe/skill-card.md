## Description:

Daily Recipe recommends Chinese, Western, and fusion recipes with ingredients, step-by-step instructions, and 30-60 minute home-cook meal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home cooks use this skill to answer what to cook today with bilingual recipe recommendations, practical ingredient lists, cooking steps, tips, and optional daily reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can set up recurring recipe push reminders with per-user local settings and multi-channel delivery.

Mitigation: Enable reminders only after confirming the recipient, channel, schedule, and whether persistent userId-based settings are acceptable.

Risk: Scheduled pushes use a fixed Asia/Shanghai timezone unless the surrounding platform changes the emitted cron configuration.

Mitigation: Review the configured reminder times and timezone before enabling daily morning or evening pushes.

Risk: Generated recipe pages may include ad-ready placeholders and ClawCode branding.

Mitigation: Review generated HTML before publishing or sharing it in contexts where advertising placeholders or branding are not desired.

## Reference(s):

- [Daily Recipe on ClawHub](https://clawhub.ai/jiajiaoy/skills/daily-recipe)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Bilingual recipe guidance, Markdown responses, and a single-file HTML recipe page.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also emit OpenClaw cron add/remove commands for scheduled morning and evening recipe pushes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
