## Description: <br>
Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway for native API calls and connection management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbright4497](https://clawhub.ai/user/mbright4497) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route agent-initiated API calls through Maton's gateway after users authorize the required OAuth connections. It is suited for workflows that need to read, write, send, share, or administer records across supported services such as Google Workspace, Microsoft 365, Slack, Notion, Airtable, and HubSpot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broker broad authenticated access to connected third-party services, including read, publish, delete, share, webhook, and admin actions. <br>
Mitigation: Install only when Maton is trusted for the connected services, connect only required services, use least-privilege OAuth scopes, and supervise high-impact actions. <br>
Risk: Agent-initiated mutations or public-facing operations can affect live business data or communications. <br>
Mitigation: Require explicit confirmation before write, delete, send, sharing, webhook, or admin operations, and verify target records before execution. <br>
Risk: The MATON_API_KEY authenticates gateway requests and must be protected from disclosure. <br>
Mitigation: Store the key in a managed secret or environment variable, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: When multiple OAuth connections exist for the same app, using the default connection can target the wrong account. <br>
Mitigation: Specify the intended connection with the Maton-Connection header for sensitive or account-specific actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbright4497/api-gateway-1-0-46) <br>
- [Maton homepage](https://maton.ai) <br>
- [API Gateway skill documentation](artifact/SKILL.md) <br>
- [Provider routing guides](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with Python and shell examples, endpoint patterns, and provider routing notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized OAuth connections for each target service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
