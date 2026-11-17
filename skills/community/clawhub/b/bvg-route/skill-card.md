## Description:

Route planning for Berlin public transport (BVG) using the v6.bvg.transport.rest API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonsantos](https://clawhub.ai/user/jaysonsantos)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan Berlin public transit journeys, check next departures, and request arrive-by or depart-at route options with concise step-by-step directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route queries may send locations, route details, and travel times to the public BVG transport.rest service.

Mitigation: Avoid including unnecessary sensitive personal details in route requests and disclose that journey lookups use the public BVG API.

Risk: Malformed datetime values in the bundled shell helper can be passed into the journey URL without URL encoding.

Mitigation: Use validated ISO 8601 datetime strings or an implementation that URL-encodes all query parameters before execution.

Risk: Journey planning can be unreliable if full stop IDs with suffixes are sent to the journeys endpoint.

Mitigation: Resolve stops first and pass base six-digit IBNR codes to the journeys endpoint.

## Reference(s):

- [v6.bvg.transport.rest API documentation](https://v6.bvg.transport.rest/api.html)
- [BVG API condensed reference](references/API.md)
- [ClawHub skill page](https://clawhub.ai/jaysonsantos/skills/bvg-route)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown route summaries with optional JSON journey details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include refresh tokens, stop IDs, journey legs, transfers, walking distance, departure times, and arrival times.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
