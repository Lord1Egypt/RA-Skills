## Description: <br>
Manage Google Ads & Meta (Facebook) Ads from your AI coding tool with MCP tools for auditing, creating, and optimizing ad accounts using natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamzifei](https://clawhub.ai/user/iamzifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketing operators, and agencies use this skill to audit and manage connected Google Ads and Meta Ads accounts through an authenticated hosted MCP service. It supports read-only reporting, campaign optimization, and account mutations that can affect budgets, statuses, ads, audiences, conversion tracking, and customer lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful Google Ads and Meta Ads account changes, including budget, status, ad, audience, conversion tracking, and customer list operations. <br>
Mitigation: Protect the ADWHIZ_API_KEY, connect only necessary ad accounts, start with read-only audits where possible, and carefully review agent approvals before any write operation. <br>
Risk: Connected advertising accounts and API keys grant access to sensitive campaign and performance data. <br>
Mitigation: Use account-level scoping, revoke access when no longer needed, and avoid exposing the API key in logs, prompts, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iamzifei/adwhiz) <br>
- [Publisher Profile](https://clawhub.ai/user/iamzifei) <br>
- [AdWhiz Homepage](https://adwhiz.ai) <br>
- [AdWhiz Documentation](https://adwhiz.ai/docs) <br>
- [AdWhiz OpenAPI Specification](https://mcp.adwhiz.ai/api/v1/openapi.json) <br>
- [AdWhiz Tool Listing](https://mcp.adwhiz.ai/api/v1/tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Natural-language responses, MCP tool calls, REST API JSON responses, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADWHIZ_API_KEY and connected Google or Meta ad accounts] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
