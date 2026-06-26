## Description: <br>
Data-driven pricing strategy engine for Amazon sellers that analyzes ASINs, pricing landscape, competitors, trends, and profit scenarios to produce RAISE, HOLD, or LOWER recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers and operators use this skill to evaluate product pricing from ASIN inputs, compare category and competitor signals, and review profit-aware pricing recommendations. It supports single-product and batch pricing analysis using APIClaw data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon ASINs, competitor context, pricing inputs, and business assumptions to APIClaw. <br>
Mitigation: Use it only with data appropriate for APIClaw processing, avoid unrelated confidential inputs, and validate recommendations with additional business sources before acting. <br>
Risk: The bundled CLI requires an APIClaw key and can consume paid or limited API credits. <br>
Mitigation: Use a dedicated APIClaw key with limited credits, store it in the APICLAW_API_KEY environment variable, and monitor reported API usage. <br>
Risk: Pricing recommendations are based on sampled API data and estimates such as lower-bound sales and estimated FBA fees. <br>
Mitigation: Treat recommendations as decision support, verify fees and current marketplace conditions, and review every RAISE, HOLD, or LOWER signal before changing prices. <br>


## Reference(s): <br>
- [Amazon Pricing Command Center](https://clawhub.ai/apiclaw/amazon-pricing-command-center) <br>
- [APIClaw API Key Setup](https://apiclaw.io/en/api-keys) <br>
- [APIClaw](https://apiclaw.io) <br>
- [APIClaw OpenAPI Base URL](https://api.apiclaw.io/openapi/v2) <br>
- [APIClaw API Docs](https://api.apiclaw.io/api-docs) <br>
- [Market Entry Analyzer API Field Reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown pricing analysis with tables, data provenance, API usage, and optional shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language matches the user's input language and includes confidence labels for conclusions.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
