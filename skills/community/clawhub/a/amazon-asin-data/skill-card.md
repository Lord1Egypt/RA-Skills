## Description: <br>
Amazon niche market analysis tool for cross-border e-commerce product selection that retrieves demand scores, competition analysis, price ranges, brand concentration, and sales metrics for US, Japan, and Germany markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctzys](https://clawhub.ai/user/ctzys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, product researchers, and developers use this skill to query Amazon niche-market data through LinkFoxAgent, compare demand, competition, pricing, and sales signals, and prepare product-selection analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product-research keywords, filters, target markets, and API usage are sent to LinkFoxAgent. <br>
Mitigation: Use the skill only when the provider's data handling terms are acceptable, avoid submitting confidential product plans, and keep the API key in the current session or a secrets manager. <br>
Risk: API keys can be exposed if copied into shared logs, screenshots, or committed configuration. <br>
Mitigation: Set LINKFOXAGENT_API_KEY through a secure environment or secrets workflow and avoid printing it in shared output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ctzys/amazon-asin-data) <br>
- [API Overview](references/API-Overview.md) <br>
- [Jiimore API Reference](references/Jiimore.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON data summaries, tables, Python examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for live API use and may include Amazon marketplace metrics, filters, and report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
