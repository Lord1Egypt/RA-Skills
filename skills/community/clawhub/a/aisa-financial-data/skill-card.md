## Description: <br>
Query real-time and historical financial data across equities and crypto-prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaPay](https://clawhub.ai/user/AIsaPay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to retrieve stock and cryptocurrency market data, financial statements, analyst estimates, insider trades, institutional ownership, SEC filings, interest rates, and screening results through the AISA API or bundled Python client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the AISA API key and requested market symbols, date ranges, filters, and portfolio-style queries to a third-party AISA endpoint. <br>
Mitigation: Use the skill only where sharing those requests with AISA is acceptable, store AISA_API_KEY as a secret, and avoid hardcoding or logging the key. <br>
Risk: Market-data calls may consume paid credits. <br>
Mitigation: Monitor usage costs and credits before using the skill in automated or high-volume workflows. <br>
Risk: Submitted queries could reveal confidential trading strategies or private portfolio details. <br>
Mitigation: Avoid sending sensitive strategies or private portfolio information unless third-party sharing has been approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIsaPay/aisa-financial-data) <br>
- [Publisher profile](https://clawhub.ai/user/AIsaPay) <br>
- [AISA API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the bundled Python client prints JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
