## Description: <br>
Provides real-time BTC/ETH/SOL prices, sentiment and technical indicators, top industry and policy news, plus trending coin prices via Desk3 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desk3](https://clawhub.ai/user/desk3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve a concise cryptocurrency market briefing from Desk3, including prices, sentiment, cycle indicators, news, calendars, exchange rates, and trending assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Node scripts contact Desk3 APIs for live public cryptocurrency market data and news. <br>
Mitigation: Install and run the skill only when outbound requests to Desk3 APIs are acceptable for the deployment environment. <br>
Risk: Market interpretations, news summaries, and buy/hold/sell-style wording may be mistaken for financial advice. <br>
Mitigation: Treat all market output as informational and require human review before making trading or investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/desk3/cryptocurrency-market-live-briefing) <br>
- [Desk3 homepage](https://www.desk3.io) <br>
- [Desk3 main market data API](https://api1.desk3.io/v1/) <br>
- [Desk3 MCP service API](https://mcp.desk3.io/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; fetches public cryptocurrency market data and news from Desk3 APIs without an API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
