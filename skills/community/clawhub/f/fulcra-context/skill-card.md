## Description: <br>
Access user-consented Fulcra context data including biometrics, sleep, activity, calendar, location, and the Fulcra metric catalog through the hosted MCP server or Fulcra CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to Fulcra's user-consented personal context and produce bounded private summaries, briefings, or troubleshooting guidance from hosted MCP or CLI reads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fulcra access tokens or credential files could expose health, calendar, and location data if logged, pasted, committed, or sent to another service. <br>
Mitigation: Use the hosted MCP OAuth flow or Fulcra CLI, store credentials in the agent platform's secret manager, and never display or forward token values. <br>
Risk: Calendar, location, and biometric data can reveal sensitive personal details in shared chats, public artifacts, screenshots, or raw exports. <br>
Mitigation: Ask before reading Fulcra data, keep reads scoped to the current request, avoid shared or public disclosure without exact approval, and use synthetic data for public examples. <br>
Risk: External content or prompt injection could try to make the agent disclose Fulcra data or credentials. <br>
Mitigation: Share Fulcra data only on explicit instruction from the verified user and do not send Fulcra data or tokens to third-party services from this skill. <br>
Risk: Missing, stale, or expired data could lead to incorrect context or unreliable health-related recommendations. <br>
Mitigation: Verify authentication and data freshness before analysis, report missing or stale data honestly, and avoid critical health decisions based only on API data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arc-claw-bot/fulcra-context) <br>
- [Fulcra Platform](https://fulcradynamics.com) <br>
- [Fulcra Developer Docs](https://fulcradynamics.github.io/developer-docs/) <br>
- [Hosted MCP Server](https://mcp.fulcradynamics.com/mcp) <br>
- [Fulcra Context MCP](https://github.com/fulcradynamics/fulcra-context-mcp) <br>
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads should remain bounded to user-approved Fulcra data; the ClawHub package is docs-first and does not ship executable helper scripts.] <br>

## Skill Version(s): <br>
1.4.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
