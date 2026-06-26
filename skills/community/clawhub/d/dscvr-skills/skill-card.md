## Description: <br>
Query DSCVR crypto intelligence APIs for market news, event tracking, smart money analysis, prediction market data, AI-powered event discovery, market orderbooks, and social graph data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dscvr-release](https://clawhub.ai/user/dscvr-release) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to query DSCVR for crypto news, prediction market intelligence, smart money trader data, orderbook depth, and DSCVR social graph records via authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DSCVR credentials are required and the secret key can authorize API access. <br>
Mitigation: Keep DSCVR_SECRET_KEY private, prefer environment variables or a secret manager, and avoid pasting credentials into prompts or shared logs. <br>
Risk: Changing DSCVR_API_BASE_URL could send authenticated requests to an untrusted endpoint. <br>
Mitigation: Use the default https://dscvr.one endpoint or another explicitly trusted DSCVR API base URL. <br>
Risk: The social GraphQL command accepts raw user-provided queries. <br>
Mitigation: Review GraphQL queries before execution and limit them to the intended DSCVR user, content, or portal data. <br>


## Reference(s): <br>
- [DSCVR Intelligence API Reference](references/api-reference.md) <br>
- [DSCVR API Authentication Reference](references/auth-reference.md) <br>
- [DSCVR API credentials](https://dscvr.one/subscription) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [ClawHub release page](https://clawhub.ai/dscvr-release/dscvr-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON-derived API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DSCVR_API_KEY and DSCVR_SECRET_KEY; queries the DSCVR API over the network.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
