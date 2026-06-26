## Description: <br>
Query Data912 public market data endpoints for Argentina and USA instruments, including MEP/CCL quotes, market panels, OHLC history, option chains, and volatility metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferminrp](https://clawhub.ai/user/ferminrp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve public Data912 market snapshots, historical OHLC data, option chains, and volatility metrics for Argentina and USA instruments. It is intended for educational, non-real-time market summaries, not financial recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced OpenAPI spec includes an unrelated contact endpoint that can send email and message text to the external service. <br>
Mitigation: Keep use limited to the documented market-data GET endpoints and do not send private messages or personal contact details through this skill. <br>


## Reference(s): <br>
- [Data912 OpenAPI spec](references/openapi-spec.json) <br>
- [Data912 API](https://data912.com) <br>
- [ClawHub skill page](https://clawhub.ai/ferminrp/data912) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Data912 endpoints without an API key; outputs should note that the data is educational and non-real-time.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
