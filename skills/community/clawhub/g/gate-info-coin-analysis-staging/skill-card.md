## Description: <br>
Single-coin comprehensive analysis for a cryptocurrency using fundamentals, market snapshot, technical analysis, news, and social sentiment data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a structured, data-driven analysis report for one cryptocurrency when they need a broad overview rather than price-only, risk-only, comparison, or technical-only output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market analysis may be mistaken for financial advice. <br>
Mitigation: Present the report as data-driven information, include the not-investment-advice warning, and avoid explicit buy/sell recommendations or price predictions. <br>
Risk: Unavailable or failed market, news, technical, or sentiment feeds could lead to incomplete analysis. <br>
Mitigation: Continue only with available feeds, clearly label unavailable dimensions, and do not fabricate missing data. <br>
Risk: Ambiguous coin names or symbols may cause analysis of the wrong asset. <br>
Mitigation: Ask the user to clarify the coin before running the analysis when the target asset cannot be identified. <br>
Risk: Broad trigger phrases may route risk-only, comparison, news-only, or technical-only requests into the wrong workflow. <br>
Mitigation: Route those requests to the dedicated specialized skill or tool path instead of stretching this single-coin comprehensive workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-coin-analysis-staging) <br>
- [Gate Info Coin Analysis Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Gate Info CoinAnalysis MCP Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, summaries, links, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses available Gate Info and Gate News data, labels missing dimensions as unavailable, and avoids buy/sell advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
