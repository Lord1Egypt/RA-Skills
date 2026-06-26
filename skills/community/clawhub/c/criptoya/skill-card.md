## Description: <br>
Queries CriptoYa for cryptocurrency prices by exchange or aggregate market view and retrieves withdrawal fee information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferminrp](https://clawhub.ai/user/ferminrp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to answer cryptocurrency price and fee questions for supported coins, fiat currencies, exchanges, and volumes by querying CriptoYa and summarizing best bid, ask, and spread. Results are informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public network requests to CriptoYa for crypto prices and fees. <br>
Mitigation: Use it only when public requests to CriptoYa are acceptable, and do not include credentials or sensitive data in queries. <br>
Risk: Unsupported pairs or invalid parameters may return non-JSON text such as "Invalid pair" with HTTP 200. <br>
Mitigation: Validate requested coins, fiat currencies, exchanges, and volume format against the documented lists, then handle invalid-pair responses explicitly. <br>
Risk: Crypto prices are time-sensitive and may vary across exchanges. <br>
Mitigation: Present the response timestamp when available and keep the output informational rather than financial advice. <br>


## Reference(s): <br>
- [CriptoYa](https://criptoya.com) <br>
- [CriptoYa fees endpoint](https://criptoya.com/api/fees) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with short tables and optional curl/jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public CriptoYa JSON responses; results are informational and should include timestamp context when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
