## Description: <br>
Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to query AIsa market data for equities and cryptocurrencies when building research, alerts, reporting, or portfolio-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AISA_API_KEY to send market queries to the AIsa API, and API usage may incur costs. <br>
Mitigation: Use a dedicated or scoped API key when available, keep the key out of prompts and logs, and monitor API usage and credit consumption. <br>
Risk: Submitted ticker, portfolio-like, or market-interest queries may be visible to the API provider. <br>
Mitigation: Submit only intended market queries and avoid including unnecessary sensitive portfolio context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bowen-dotcom/aisa-market-skill) <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python client commands, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; sends user-requested market queries to the AIsa API and may incur API costs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
