## Description:

Plan multi-waypoint journeys with route optimization, feasibility analysis, and time budget constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Journey to plan and validate multi-stop trips, estimate travel time, and check whether waypoint itineraries fit transport and time-budget constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Waypoint coordinates and purpose notes are sent to Camino's hosted API.

Mitigation: Avoid sending sensitive itinerary details unless the user accepts the data-sharing implications.

Risk: The skill depends on a Camino API key and local command-line tools.

Mitigation: Store and rotate CAMINO_API_KEY as a service credential, and install curl and jq from trusted sources.

Risk: Installer and helper commands can affect the local environment.

Mitigation: Install only trusted publisher versions and avoid elevated privileges for installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-journey)
- [ClawHub publisher profile](https://clawhub.ai/user/james-southendsolutions)
- [Camino API activation](https://app.getcamino.ai/skills/activate)
- [Camino Journey API endpoint](https://api.getcamino.ai/journey)
- [x402 payment protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script sends JSON waypoint data to Camino's hosted Journey API and formats the JSON response with jq.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
