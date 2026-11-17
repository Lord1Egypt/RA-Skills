## Description:

Live flight tracking and aviation data via FlightAware AeroAPI through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and travelers use this skill to retrieve live flight, airport, operator, aircraft, schedule, and alert information through FlightAware AeroAPI. It supports tracking flights, checking airport activity, and managing flight alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup requires an AeroAPI key in the MCP configuration.

Mitigation: Review the MCP setup configuration and store the key in a protected secret or environment variable.

Risk: AeroAPI requests use the account's subscription quota and may incur query charges.

Mitigation: Check the account's plan and remaining quota before repeated lookups.

Risk: Creating, updating, or deleting alerts changes the FlightAware account's alert settings.

Mitigation: Review the alert details and confirm the change before it is submitted.

## Reference(s):

- [FlightAware MCP package](https://www.npmjs.com/package/@chrischall/flightaware-mcp)
- [FlightAware AeroAPI portal](https://www.flightaware.com/aeroapi/portal/)

## Skill Output:

**Output Type(s):** [Text, Structured data, Images]

**Output Format:** [Structured AeroAPI responses, text summaries, and PNG flight maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results depend on AeroAPI access, subscription tier, quota, and service availability.]

## Skill Version(s):

1.4.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
