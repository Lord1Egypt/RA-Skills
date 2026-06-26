## Description: <br>
Runs a local script to fetch economic calendar events for a date range, using TradingEconomics when TRADING_ECONOMICS_API_KEY is present and Yahoo Finance otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve forward-looking macroeconomic calendar events for today, this week, or a custom date range before trading or planning market analysis. It can also help set up recurring daily economic calendar briefings through a separate reminder workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact TradingEconomics or Yahoo Finance to fetch calendar data. <br>
Mitigation: Install and run it only in environments where external calendar-data requests to those services are acceptable. <br>
Risk: The optional TradingEconomics credential can be exposed if stored carelessly in a repository .env file. <br>
Mitigation: Prefer TRADING_ECONOMICS_API_KEY in the runtime environment; if a .env file is used, keep it gitignored and limited to this credential. <br>
Risk: Recurring calendar briefings can continue running after they are no longer needed. <br>
Mitigation: Review the recurring briefing before confirming it and manage or cancel it through the remind-me workflow. <br>
Risk: Yahoo Finance fallback results may omit importance, forecast, or market-expectation fields and may return country codes instead of full country names. <br>
Mitigation: Treat fallback output as lower-detail calendar guidance and use TradingEconomics credentials when richer metadata is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youpele52/economic-calendar-pro) <br>
- [TradingEconomics economic calendar snapshot documentation](https://docs.tradingeconomics.com/economic_calendar/snapshot/) <br>
- [TradingEconomics API base URL](https://api.tradingeconomics.com) <br>
- [Yahoo Finance calendar events fallback endpoint](https://query1.finance.yahoo.com/ws/screeners/v1/finance/calendar-events) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text calendar report with grouped events and markdown command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and optionally TRADING_ECONOMICS_API_KEY; without the key, output uses the Yahoo Finance fallback with reduced metadata.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
