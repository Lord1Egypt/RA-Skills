## Description: <br>
Live flight tracking and aviation data via FlightAware AeroAPI through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and aviation users use this skill to configure an MCP-backed assistant for FlightAware AeroAPI queries, including flight status, aircraft positions, airport activity, schedules, aircraft ownership, and alert management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AeroAPI requests use the user's API key and can count against quota or billing. <br>
Mitigation: Use only the intended AeroAPI key, review expected query volume, and configure cache TTL settings to reduce repeated billable requests. <br>
Risk: Alert-management tools can modify FlightAware account alert settings when explicitly confirmed. <br>
Mitigation: Review dry-run previews first and require explicit confirmation only for intended alert changes. <br>
Risk: The setup runs an external npm package. <br>
Mitigation: Review the package or source before installing and pin the package version when stable deployments require repeatability. <br>


## Reference(s): <br>
- [FlightAware MCP npm package](https://www.npmjs.com/package/@chrischall/flightaware-mcp) <br>
- [FlightAware AeroAPI portal](https://www.flightaware.com/aeroapi/portal/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to call MCP tools that use the user's AeroAPI key; flight-map output can create PNG files in the configured output directory.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
