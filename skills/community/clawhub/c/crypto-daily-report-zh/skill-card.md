## Description:

Generate and send cryptocurrency daily reports with market overview, fear & greed index, liquidation data, economic calendar, and news aggregation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renyuke-cn](https://clawhub.ai/user/renyuke-cn)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate Chinese-language cryptocurrency daily briefings and optionally schedule delivery to Telegram or Discord channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure recurring Telegram delivery to a fixed or unintended channel without clear confirmation or removal controls.

Mitigation: Before enabling scheduling, replace the default Telegram ID with a destination the user controls, confirm the exact target and cadence, and document how to list and remove the cron job.

Risk: Generated cryptocurrency market reports may be incomplete, stale, or mistaken for financial advice.

Mitigation: Treat reports as informational, keep the investment-risk disclaimer, and verify material market information against cited sources before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renyuke-cn/skills/crypto-daily-report-zh)
- [Fear & Greed Index API](https://api.alternative.me/fng/?limit=2)
- [Cointelegraph RSS](https://cointelegraph.com/rss)
- [TokenInsight RSS](https://tokeninsight.com/rss/news)
- [Incrypted Calendar](https://incrypted.com/en/calendar/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown report with optional shell commands for scheduled delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public market data, RSS feeds, calendar content, and messaging-channel delivery targets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
