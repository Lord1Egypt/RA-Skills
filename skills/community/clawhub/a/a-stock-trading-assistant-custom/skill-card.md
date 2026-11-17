## Description:

A Stock Trading Assistant Custom provides Mainland China A-share market quotes, individual stock analysis, market sentiment, hot-sector tracking, trading strategy suggestions, and price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review Mainland China A-share stocks, retrieve real-time quotes, index and sector data, and draft informational trading strategies or price alerts with risk reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete trading suggestions that may be mistaken for personalized investment advice.

Mitigation: Treat outputs as informational, verify decisions through trusted sources, and do not rely on position sizing or buy/sell guidance as personalized advice.

Risk: The skill queries third-party Chinese financial sites through unauthenticated requests, so prices may be stale, unavailable, or inconsistent.

Mitigation: Show the data source and retrieval time, cross-check prices with trusted market-data sources, and handle failed or incomplete requests conservatively.

Risk: Price alerts and watchlist details may reveal a user's trading interests if persisted.

Mitigation: Store only the alert details needed for the task, avoid sensitive account information, and clear watchlist data when it is no longer needed.

## Reference(s):

- [A Stock Trading Assistant Custom on ClawHub](https://clawhub.ai/c595390153-a11y/skills/a-stock-trading-assistant-custom)
- [Individual Stock Analysis Method Reference](references/analysis.md)
- [Data Source API Reference](references/data-sources.md)
- [Sina Finance](https://finance.sina.com.cn)
- [Eastmoney](https://www.eastmoney.com)
- [Tonghuashun](https://www.10jqka.com.cn)
- [Xueqiu](https://xueqiu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text, with optional JSON from the bundled stock-fetching script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label data source and retrieval time and include risk reminders for price or trading suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
