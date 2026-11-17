## Description:

Daily financial news briefing — stock markets, crypto, macro economy, Fed/PBOC policy, earnings reports. Bilingual EN/CN visual dashboard. Morning push + evening recap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Dailyfinance to generate bilingual EN/CN daily finance briefings and visual dashboards covering equities, crypto, macroeconomics, central bank policy, and earnings. It can also configure morning and evening push recaps to supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling push delivery creates recurring morning and evening scheduled messages to the selected channel.

Mitigation: Review the selected channel and schedule before enabling pushes, use the status command to audit settings, and use the documented off command to disable recurring messages.

Risk: Push configuration stores a local userId and schedule preferences.

Mitigation: Use non-sensitive user identifiers, limit access to local skill data, and disable or remove stored preferences when push delivery is no longer needed.

Risk: Financial market data and news summaries may be delayed, incomplete, or unsuitable as investment advice.

Mitigation: Keep source attribution, delayed-data notices, neutral tone, and the financial disclaimer in generated dashboards.

Risk: Generated HTML may include ad placeholders and fixed branding that are not appropriate for every deployment.

Mitigation: Review the generated HTML before publishing and remove or adjust ad slots and branding where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiajiaoy/skills/dailyfinance)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and a generated single-file HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write /mnt/user-data/outputs/daily-finance.html and emit OpenClaw cron add/remove directives for push scheduling.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
