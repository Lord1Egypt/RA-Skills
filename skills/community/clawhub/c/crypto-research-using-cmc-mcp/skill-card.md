## Description:

Performs comprehensive due diligence on a cryptocurrency using CoinMarketCap MCP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryan-cmc](https://clawhub.ai/user/bryan-cmc)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to research a specific cryptocurrency beyond price, combining CoinMarketCap MCP market data, token metadata, holder metrics, technical indicators, and recent news into a balanced report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research reports may be mistaken for financial advice when users ask investment-style questions.

Mitigation: Frame outputs as research, not financial advice, and present both positive and negative findings.

Risk: CoinMarketCap MCP credentials could be mishandled during setup.

Mitigation: Configure the API key only through MCP settings and avoid placing secrets in generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bryan-cmc/skills/crypto-research-using-cmc-mcp)
- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp)
- [CoinMarketCap API key setup](https://pro.coinmarketcap.com/login)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown research report with structured sections and optional JSON configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CoinMarketCap MCP data and should note missing or unavailable data explicitly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
