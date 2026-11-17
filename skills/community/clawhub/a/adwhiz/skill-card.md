## Description:

Manage Google Ads & Meta (Facebook) Ads from your AI coding tool with MCP tools for auditing, creating, and optimizing ad accounts using natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketing operators, and agencies use AdWhiz to connect an AI coding tool to Google Ads and Meta Ads accounts for campaign audits, reporting, optimization, and account changes through a hosted MCP or REST interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted connector can read and change connected Google Ads and Meta Ads accounts, including budget changes, activation or removal actions, and customer list uploads.

Mitigation: Connect only intended ad accounts, review each write confirmation carefully, and revoke AdWhiz access when it is no longer needed.

Risk: The skill depends on an ADWHIZ_API_KEY that authorizes access to the user's connected ad accounts.

Mitigation: Store the API key only in the agent's secret or environment configuration and rotate it if it may have been exposed.

## Reference(s):

- [AdWhiz Homepage](https://adwhiz.ai)
- [AdWhiz Documentation](https://adwhiz.ai/docs)
- [AdWhiz OpenAPI Specification](https://mcp.adwhiz.ai/api/v1/openapi.json)
- [AdWhiz Tool Listing](https://mcp.adwhiz.ai/api/v1/tools)
- [ClawHub Skill Page](https://clawhub.ai/iamzifei/skills/adwhiz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger hosted MCP or REST calls that read or change connected Google Ads and Meta Ads accounts after user authorization.]

## Skill Version(s):

2.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
