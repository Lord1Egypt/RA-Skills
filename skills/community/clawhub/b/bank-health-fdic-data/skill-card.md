## Description: <br>
Bank Health & FDIC Data helps agents check US bank financial health, FDIC-active status, assets, and deposits using FDIC institution data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents, fintech teams, treasury workflows, and risk analysts use this skill to check FDIC-active status and financial health signals for US banks before transacting or screening banking partners. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes agents to a paid external API call using x402 USDC payment. <br>
Mitigation: Confirm the bank query and expected charge before allowing wallet auto-payment or repeated calls. <br>
Risk: Bank health outputs may be used for financial or counterparty-risk decisions. <br>
Mitigation: Treat the returned FDIC data as one input to due diligence and verify material decisions against authoritative banking and compliance sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colinhughes2121/bank-health-fdic-data) <br>
- [GoCreative bank risk API endpoint](https://api.gocreativeai.com/v1/risk/bank/{name}) <br>
- [GoCreative Agent Compliance & Data API](https://api.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance describing an HTTPS GET endpoint and the expected JSON API response.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The endpoint uses x402 USDC payment on Base through an OpenClaw wallet and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
