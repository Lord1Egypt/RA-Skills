## Description: <br>
Rebuilds the current A-share market session from fresh data by reviewing indices, breadth, turnover, sectors, sentiment, and leading stocks to create a session-scoped market work package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minguncle](https://clawhub.ai/user/minguncle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to reconstruct the current A-share trading session, identify market breadth and sector leadership, and prepare a session-scoped watchlist or trading framework. It is analysis support and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market analysis may be mistaken for financial advice or acted on without independent review. <br>
Mitigation: Treat outputs as analysis support, verify current data and assumptions, and apply the user's own investment policy before trading. <br>
Risk: Current-market conclusions can become stale quickly during an active trading session. <br>
Mitigation: Refresh source data when the user asks about today, now, or just-finished market conditions, and note the timestamp or session phase used. <br>


## Reference(s): <br>
- [Sweep Order](references/sweep-order.md) <br>
- [ClawHub skill page](https://clawhub.ai/minguncle/a-share-market-sweep) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown sections covering conclusion, evidence, temporary market database, trading framework, risk list, and watchlist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on current web or stock-data retrieval when invoked; outputs should be checked against current market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
