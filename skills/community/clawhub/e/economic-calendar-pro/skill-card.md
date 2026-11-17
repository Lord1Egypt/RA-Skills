## Description:

Run a local script to fetch economic calendar events for a date range. Defaults to 7 days inclusive from the query day. Uses TradingEconomics when TRADING_ECONOMICS_API_KEY is present and falls back to Yahoo Finance otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch scheduled macroeconomic calendar events for a default seven-day window or a specified date range. It can also guide setup of recurring daily economic calendar briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and .env handling is broader than documented, and the TradingEconomics credential may appear in provider or proxy URL logs.

Mitigation: Run from a controlled directory, use a narrowly scoped TradingEconomics key, avoid placing unrelated secrets in nearby .env files, and rotate the key if logs are exposed.

Risk: Recurring briefing setup creates a remind-me cron that can continue running and delivering calendar output.

Mitigation: Confirm the schedule, timezone, destination channel, and cancellation path before creating the reminder; periodically list and remove unused reminders.

Risk: The Yahoo Finance fallback can omit importance, forecast, and market-expectation fields or return country codes, reducing data completeness.

Mitigation: Prefer a valid TradingEconomics API key when those fields matter, and label fallback output as lower fidelity for downstream decisions.

## Reference(s):

- [TradingEconomics Economic Calendar API documentation](https://docs.tradingeconomics.com/economic_calendar/snapshot/)
- [Yahoo Finance economic calendar fallback endpoint](https://query1.finance.yahoo.com/ws/screeners/v1/finance/calendar-events)
- [ClawHub release page](https://clawhub.ai/youpele52/skills/economic-calendar-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown with inline shell commands and formatted calendar entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts optional start and end dates; uses a TradingEconomics credential when configured and otherwise falls back to lower-fidelity Yahoo Finance data.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
