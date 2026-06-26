## Description: <br>
Compares two to five cryptocurrencies using Gate Info market snapshots, coin fundamentals, and optional technical analysis to produce a side-by-side report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare two to five crypto assets across market metrics, fundamentals, and technical signals. It supports neutral, data-driven comparison reports while avoiding buy/sell recommendations and price predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto comparison output may be mistaken for investment advice. <br>
Mitigation: Keep analysis neutral and data-driven, avoid buy/sell recommendations or price predictions, and include a not-investment-advice disclaimer. <br>
Risk: Market, fundamentals, or technical data may be missing or temporarily unavailable from the Gate Info MCP provider. <br>
Mitigation: Label unavailable dimensions clearly, continue with remaining data when possible, and avoid false rankings when data is incomplete. <br>
Risk: Users may include private portfolio, account, or trading details in prompts. <br>
Mitigation: Advise users to avoid private financial details unless they intend those details to be used in the comparison. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gate-exchange/gate-info-coin-compare) <br>
- [Gate Info Coin Compare Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Gate Info CoinCompare MCP Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison report with tables, summary, dimension-by-dimension notes, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Gate Info MCP market and coin data; marks unavailable dimensions instead of fabricating data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
