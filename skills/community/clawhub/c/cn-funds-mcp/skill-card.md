## Description: <br>
China fund and stock data assistant for querying fund valuation, NAV, holdings, manager information, stock and index quotes, capital flows, sector rankings, northbound capital, and locally managed fund portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallke](https://clawhub.ai/user/smallke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this MCP skill to retrieve China fund, stock, index, and market-flow data and to maintain local fund portfolio and reminder records for analysis. It can also support screenshot-assisted portfolio import when the host model provides OCR or image understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio and reminder features store fund codes, shares, cost basis, and reminders in local JSON files. <br>
Mitigation: Install only if local storage of this financial context is acceptable, and review or delete the local data files when memory is no longer needed. <br>
Risk: Fund and stock identifiers are sent to public market-data APIs when the tools query live or historical data. <br>
Mitigation: Avoid sending account numbers, balances, or other unnecessary personal financial information; use only the identifiers needed for the query. <br>
Risk: Screenshot-assisted import can expose sensitive portfolio details to the host model or OCR workflow. <br>
Mitigation: Redact account numbers, balances, and unrelated personal information before using screenshot import. <br>
Risk: The skill can produce add, reduce, or stop-profit suggestions based on market and portfolio data. <br>
Mitigation: Treat all portfolio and trading suggestions as informational analysis, not professional investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smallke/cn-funds-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/smallke) <br>
- [EastMoney data source](https://www.eastmoney.com/) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [MCP tool responses as text containing JSON data, summaries, reminders, and informational portfolio guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include real-time or estimated market data from public APIs and locally stored portfolio or reminder records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
