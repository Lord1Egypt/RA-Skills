## Description:

Use when an agent or member needs to know what its own ~alter account can currently do, what raises its tier next, or why a call just failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, members, and operators use this skill to check the authenticated ~alter account's handle, key validity, scopes, trust tier, activity portfolio, and privacy-budget context before or after Alter MCP calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an Alter API key to Alter's hosted MCP service as an authentication header.

Mitigation: Install it only when using Alter's hosted MCP service, keep ALTER_API_KEY secret, and send it only to the disclosed Alter MCP endpoint.

Risk: Tool calls can reveal account status, scopes, trust standing, and Alter portfolio information for the authenticated key.

Mitigation: Use the status outputs for troubleshooting and access planning, and avoid sharing returned account or portfolio details outside the intended operational context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-my-standing)
- [Alter hosted MCP server](https://mcp.truealter.com/api/v1/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tool names, endpoint configuration, and credential-handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALTER_API_KEY for authenticated Alter MCP calls]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
