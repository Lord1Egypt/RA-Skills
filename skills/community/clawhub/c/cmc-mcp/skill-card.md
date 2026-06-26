## Description: <br>
Fetches cryptocurrency market data, prices, technical analysis, news, and trends using the CoinMarketCap MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to answer cryptocurrency market questions with CoinMarketCap MCP data, including prices, market metrics, technical indicators, news, and macro events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto-related prompts may be sent to CoinMarketCap's external MCP service even when live data was not clearly requested. <br>
Mitigation: Use the skill only for explicit live market-data requests, and avoid sending sensitive portfolio, account, or trading details unless necessary. <br>
Risk: The skill requires a CoinMarketCap API key and API usage may be subject to quota or cost limits. <br>
Mitigation: Store the API key only in MCP server configuration, restrict access to that configuration, and monitor CoinMarketCap API usage. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bryan-cmc/cmc-mcp) <br>
- [CoinMarketCap skill homepage](https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap) <br>
- [CoinMarketCap API key setup](https://pro.coinmarketcap.com/login) <br>
- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown answers with optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market data, technical indicators, news summaries, and MCP setup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
