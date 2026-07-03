## Description: <br>
Access user-consented Fulcra context data including biometrics, sleep, activity, calendar, location, and the Fulcra metric catalog through the hosted MCP server or Fulcra CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Fulcra Context to let agents retrieve bounded, user-consented Fulcra health, activity, calendar, location, and metric catalog context for private briefings, summaries, and scoped analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fulcra data can include sensitive health, calendar, and location context. <br>
Mitigation: Ask before reading Fulcra data, keep reads scoped to the current request, and avoid exposing raw records or identifying context unless the user explicitly approves that disclosure. <br>
Risk: Access tokens, refresh tokens, credential files, or capability URLs could allow unauthorized access if exposed. <br>
Mitigation: Use the hosted MCP OAuth flow or Fulcra CLI authentication, never print or share token values, and keep credentials out of logs, public files, and third-party services. <br>
Risk: Calendar and location data can identify private places, meetings, attendees, and routines. <br>
Mitigation: Use calendar and location only in private sessions or with explicit approval, and prefer synthetic data for public examples, screenshots, demos, tests, and documentation. <br>
Risk: Stale or missing Fulcra data can lead to misleading summaries or recommendations. <br>
Mitigation: Check data freshness with bounded update or record queries when available, report missing data honestly, and avoid making critical health decisions from API data alone. <br>


## Reference(s): <br>
- [Fulcra Platform](https://fulcradynamics.com) <br>
- [Fulcra Developer Docs](https://fulcradynamics.github.io/developer-docs/) <br>
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python) <br>
- [Fulcra Context MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bounded read guidance and command patterns; it does not ship executable helper scripts in the ClawHub package.] <br>

## Skill Version(s): <br>
1.4.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
