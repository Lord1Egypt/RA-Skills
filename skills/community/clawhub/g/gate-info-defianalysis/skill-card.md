## Description: <br>
Provides DeFi ecosystem analysis through Gate Info MCP for TVL rankings, protocol metrics, yield/APY, stablecoins, bridges, exchange reserves, and liquidation heatmaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route DeFi platform-metrics questions to read-only Gate Info MCP tools and produce neutral, data-driven analysis. It is intended for informational DeFi research, not financial advice or trade recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Gate Info MCP data source, so unavailable or untrusted MCP access can produce missing or unreliable analysis. <br>
Mitigation: Confirm the Gate Info MCP server is installed and trusted before use; if tools are missing or fail, degrade gracefully and label unavailable data. <br>
Risk: Yield, reserve, liquidation, and protocol metrics can be mistaken for financial advice or guarantees. <br>
Mitigation: Treat outputs as informational market data, avoid buy/sell recommendations, and state that APY, reserves, and liquidation levels are historical or estimated signals. <br>
Risk: DeFi protocols and yield pools can carry smart contract, liquidity, and market risks that are not fully captured by the returned metrics. <br>
Mitigation: Present analysis neutrally, include relevant DeFi risk caveats, and require users to perform independent review before acting on the information. <br>


## Reference(s): <br>
- [Gate Info DeFi Analysis Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/gate-exchange/gate-info-defianalysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analytical reports with summary metrics, ranked tables, concise analysis, and disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate Info MCP results and does not produce code, shell commands, configuration changes, or local files during normal execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
