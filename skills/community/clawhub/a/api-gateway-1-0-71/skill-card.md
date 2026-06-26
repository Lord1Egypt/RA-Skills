## Description: <br>
Connects an agent to 100+ third-party APIs through Maton's managed OAuth gateway, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaopei123](https://clawhub.ai/user/gaopei123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when they want an agent to call native endpoints on connected SaaS services, manage OAuth-backed service connections, and route requests through a unified gateway. It is suited for workflows that intentionally need live access to external accounts authorized by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad live access to many connected services. <br>
Mitigation: Install only when this gateway is intended, use least-privilege Maton connections, and restrict use to services the user has explicitly authorized. <br>
Risk: API calls can send, write, delete, bill, administer, share permissions, configure webhooks, or access cross-user data. <br>
Mitigation: Require explicit confirmation before sensitive or destructive actions and treat every request as a real action on a live third-party account. <br>
Risk: When multiple accounts are connected for the same app, routing through the wrong connection can affect the wrong account. <br>
Mitigation: Specify the exact connection ID for workflows where account selection matters. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/gaopei123/api-gateway-1-0-71) <br>
- [Maton Homepage](https://maton.ai) <br>
- [API Gateway Skill Documentation](artifact/SKILL.md) <br>
- [Supported Service References](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, HTTP request examples, and JSON request or response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; requests may operate on live third-party accounts through user-authorized connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
