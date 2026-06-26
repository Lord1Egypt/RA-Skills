## Description: <br>
Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisaDevco](https://clawhub.ai/user/aisaDevco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to retrieve stock and cryptocurrency market data, financial statements, metrics, analyst information, SEC filings, screen results, and rate data through AIsa API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an AISA_API_KEY and submitted market queries to the AIsa API. <br>
Mitigation: Use a dedicated API key where possible, monitor usage, and avoid submitting proprietary investment screens, portfolio details, or sensitive research criteria unless sharing them with AIsa is acceptable. <br>
Risk: Market data requests may create usage costs or consume credits. <br>
Mitigation: Monitor returned usage information and account costs before running broad screens, historical pulls, or repeated automated queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisaDevco/aisa-financial-data-api) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl and Python command examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to the AIsa API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
