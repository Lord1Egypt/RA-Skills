## Description: <br>
Access Coupler.io data flows configured with an OpenClaw destination to list flows, inspect schemas, and query data through an OAuth-secured read-only API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nika-is-nika](https://clawhub.ai/user/nika-is-nika) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to connect an agent to approved Coupler.io dataflows, inspect available schema details, and run read-only SQL queries against flow execution data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores OAuth tokens locally so the agent can query approved Coupler.io flows. <br>
Mitigation: Authenticate only with a Coupler.io account whose OpenClaw-destination dataflows are appropriate for agent access, and clear or reset tokens when access should be revoked. <br>
Risk: A user could authenticate against an unexpected OAuth prompt or endpoint. <br>
Mitigation: Verify the Coupler.io OAuth prompt and the auth.coupler.io and mcp.coupler.io endpoints before installation or re-authentication. <br>
Risk: Queries can expose data from all visible OpenClaw-destination flows for the authenticated account. <br>
Mitigation: Sample schemas and rows first, limit queries, and use an account scoped to dataflows the agent is allowed to inspect. <br>


## Reference(s): <br>
- [Coupler.io Skill Page](https://clawhub.ai/nika-is-nika/coupler-io) <br>
- [Coupler.io Homepage](https://coupler.io) <br>
- [mcporter CLI](https://github.com/openclaw/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP data access; responses depend on the user's authenticated Coupler.io account and configured OpenClaw-destination dataflows.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
