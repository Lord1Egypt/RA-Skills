## Description:

Fetch reusable cryptocurrency realtime spot prices and historical price/K-line data for a symbol or coin id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoworldb1](https://clawhub.ai/user/cryptoworldb1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch reusable cryptocurrency spot prices and historical candle or market-chart data for a requested symbol or coin id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected artifact references a bundled Node script and a data-source reference file that were not included in the evidence bundle.

Mitigation: Review the installed package contents before execution and confirm the referenced files are present and expected.

Risk: The skill can fetch public crypto market data and optionally write JSON output files.

Mitigation: Run it only when external market-data requests and requested file writes are acceptable for the workspace.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/cryptoworldB1/skills/tree/main/crypto-market-data)
- [Source repository](https://github.com/cryptoworldB1/skills)
- [ClawHub listing](https://clawhub.ai/cryptoworldb1/skills/crypto-market-data-2)

## Skill Output:

**Output Type(s):** [Shell commands, Code, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell and JavaScript code blocks; script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public Binance or CoinGecko market data and optionally write requested JSON files.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
