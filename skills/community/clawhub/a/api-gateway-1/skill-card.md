## Description: <br>
Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kdegeek](https://clawhub.ai/user/kdegeek) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to make authenticated calls to external services such as Google Workspace, Microsoft 365, Notion, Slack, Airtable, and HubSpot through Maton's managed OAuth connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated access to many third-party services. <br>
Mitigation: Use only with accounts and OAuth scopes the user is comfortable granting to an agent, and review the skill before installation. <br>
Risk: Delete, send, share, admin, billing, advertising, and webhook setup actions may have destructive or high-impact effects. <br>
Mitigation: Require explicit confirmation of the exact service, account, action, object IDs, recipients, and destination URLs before execution. <br>
Risk: The MATON_API_KEY authenticates requests to Maton and can be misused if exposed. <br>
Mitigation: Store the key in an environment variable or secret manager, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kdegeek/api-gateway-1) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [Provider Routing References](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks plus JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized OAuth connections for target services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
