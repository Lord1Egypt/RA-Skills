## Description: <br>
eToro Public API — full trading, market data, social, and watchlist integration. Supports SSO, Bearer, and API key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoniassia](https://clawhub.ai/user/yoniassia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent interact with eToro market data, portfolio data, trading execution, social feed, and watchlist workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live financial trading authority by default. <br>
Mitigation: Use demo or read-only credentials where possible and require manual confirmation outside the skill before any real trade or order cancellation. <br>
Risk: The skill can create public posts and comments through eToro social endpoints. <br>
Mitigation: Require manual confirmation outside the skill before publishing posts or comments. <br>
Risk: Credential-bearing request logs may expose sensitive account access details. <br>
Mitigation: Avoid casual use of live-trading credentials and review or redact logs before sharing them. <br>


## Reference(s): <br>
- [eToro Public API documentation](https://etoro-6fc30280.mintlify.app/) <br>
- [eToro Public API base URL](https://public-api.etoro.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/yoniassia/etoro-trading-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with endpoint details and command-ready API instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require curl and python3; supports SSO bearer tokens, SSO auth tokens, or API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
