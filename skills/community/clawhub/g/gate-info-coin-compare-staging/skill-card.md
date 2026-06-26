## Description: <br>
Coin comparison. Use this skill whenever the user asks to compare two or more coins. Trigger phrases include: compare, versus, vs, which is better, difference. MCP tools: info_marketsnapshot_get_market_snapshot, info_coin_get_coin_info per coin (or batch/search when available). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compare two to five crypto assets side by side using Gate Info MCP market snapshots, fundamentals, rankings, and optional technical signals. It produces neutral, data-driven comparison tables and summaries rather than trading recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad comparison wording such as 'vs' or 'which is better' may invoke the skill outside a clearly scoped crypto comparison. <br>
Mitigation: Use the skill only when two to five crypto assets are clearly identified; otherwise ask the user to clarify the assets or route to the appropriate skill. <br>
Risk: Crypto comparison output could be mistaken for financial advice or trading authorization. <br>
Mitigation: Keep the report neutral and data-driven, avoid buy/sell recommendations and price predictions, and include the not-investment-advice disclaimer required by the artifact. <br>
Risk: Missing or failed MCP data can make side-by-side comparisons misleading. <br>
Mitigation: Label unavailable dimensions clearly, continue only with available data, and stop with a concise failure summary if all required tools fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-coin-compare-staging) <br>
- [Gate Info Coin Compare Runtime Rules](artifact/references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md) <br>
- [Gate Info CoinCompare MCP Specification](artifact/references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison report with tables and concise analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate Info MCP data; marks unavailable data instead of fabricating values and includes a not-investment-advice disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter version 2026.4.6-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
