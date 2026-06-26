## Description: <br>
Use Finnhub-backed market intelligence through the `aigroup-finnhub-mcp` server for stock, crypto, forex, calendar, news, sentiment, filing, ownership, analyst, and technical-analysis tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route ticker, crypto, forex, filing, sentiment, ownership, analyst, calendar, and technical-analysis requests through a Finnhub-backed MCP server. It is suited for event-driven market research briefs where the agent should summarize signal quality rather than only relay raw data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data requests may cross an external MCP tool boundary and can include confidential portfolio, client, or nonpublic business information. <br>
Mitigation: Review and trust the external MCP package before use, prefer pinned versions where possible, and avoid sending confidential or nonpublic information unless that tool boundary is acceptable. <br>
Risk: Finance research outputs can be incomplete, stale, or misleading if interpreted as investment advice. <br>
Mitigation: Use the skill for research support, check source freshness and date ranges, and have a qualified reviewer validate conclusions before acting on them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jackdark425/aigroup-finnhub-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/jackdark425) <br>
- [Project homepage](https://github.com/jackdark425/aigroup-finnhub-mcp) <br>
- [Finnhub MCP Capabilities](references/capabilities.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text market-research summaries with referenced Finnhub signal categories] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticker symbols, date ranges, asset-class routing, and summaries of news, filings, sentiment, ownership, analyst, calendar, crypto, forex, or technical-analysis signals.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
