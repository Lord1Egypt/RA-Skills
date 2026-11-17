## Description:

AIMPACT Prediction Market monitors prediction markets such as Polymarket, identifies popular events, unusual trades, probability movement, and possible trading opportunities, and can format alerts for manual queries or configured push channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesmenews](https://clawhub.ai/user/jamesmenews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query or monitor prediction-market activity and receive concise Chinese-language alerts about popular events, large trades, probability swings, and potential trading opportunities. Push delivery is optional and depends on preconfigured OpenClaw message channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled monitoring can create indefinite background OpenClaw runs with repeated API and message activity.

Mitigation: Only add cron or Windows scheduled tasks intentionally; define an end date, monitor message/API volume, and keep a removal command ready.

Risk: Prediction-market alerts and trading-opportunity summaries can be mistaken for financial advice.

Mitigation: Treat outputs as informational signals only and review decisions manually before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamesmenews/skills/aimpact-prediction-market)
- [Publisher profile](https://clawhub.ai/user/jamesmenews)
- [MetaEra Prediction flash API](https://agent.me.news/skill/flash/list?page=1&size=20&category=prediction)
- [ME News Poly Events API](https://agent.me.news/skill/poly/events?page=1&size=20&active_only=true)
- [Alert format reference](artifact/format.md)
- [Source configuration](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown alert text with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language alert formats; optional push delivery requires externally configured OpenClaw message channels]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
