## Description: <br>
Connect to 100+ APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton's managed API gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andre-thedev](https://clawhub.ai/user/andre-thedev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to route authenticated requests to many third-party service APIs through Maton-managed connections. It is suited for workflows that need to list, create, read, update, or delete resources in connected external services after the user has authorized the relevant accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live write, delete, send, publish, billing, permission, and admin actions against connected services. <br>
Mitigation: Require explicit user confirmation before high-impact requests and verify service name, account, endpoint, target IDs, payload, and connection ID before execution. <br>
Risk: Some integrations may use API-key based authentication even though the top-level description emphasizes OAuth. <br>
Mitigation: Review each integration's documented credential method and scopes before connecting it, and avoid granting broader access than the workflow requires. <br>
Risk: Maton brokers access to external services through the MATON_API_KEY and user-authorized connections. <br>
Mitigation: Install only where Maton is trusted, store MATON_API_KEY as a secret, rotate it if exposed, and remove unused or stale connections. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/andre-thedev/api-gateway-1-0-70) <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [API Gateway skill source link](https://github.com/maton-ai/api-gateway-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and active user-authorized service connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
