## Description: <br>
Connect to 100+ APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton's managed OAuth API gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call native third-party API endpoints through a single gateway after the user authorizes the relevant service connection. It is suited for workflows that need managed OAuth access to external SaaS services without embedding each service's token directly in the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad live access to connected third-party accounts. <br>
Mitigation: Use least-privilege service connections and only connect accounts needed for the workflow. <br>
Risk: Actions such as sending, posting, deleting, sharing, billing, or administration may affect external services. <br>
Mitigation: Require explicit user confirmation before any high-impact or irreversible action. <br>
Risk: Authentication methods and scopes may vary by service. <br>
Mitigation: Review each service connection's OAuth, API key, or Basic auth behavior before authorizing it. <br>


## Reference(s): <br>
- [Maton Homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [API Gateway Skill Repository](https://github.com/maton-ai/api-gateway-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/19-api-gateway) <br>
- [Slack Reference](references/slack/README.md) <br>
- [Google Mail Reference](references/google-mail/README.md) <br>
- [GitHub Reference](references/github/README.md) <br>
- [Notion Reference](references/notion/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and user-authorized service connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
