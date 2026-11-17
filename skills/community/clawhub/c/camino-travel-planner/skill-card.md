## Description:

Plan complete day trips, walking tours, and multi-stop itineraries with time budgets using Camino AI's journey planning and route optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, travel planners, and agents use this skill to plan day trips, walking tours, business meeting routes, and multi-stop itineraries from waypoint JSON and travel constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Waypoint details, route purposes, preferences, and trip constraints are sent to Camino's external API.

Mitigation: Use the skill only for itineraries you are comfortable sending to Camino, and avoid sensitive locations unless that sharing is approved.

Risk: The skill requires CAMINO_API_KEY in the local agent environment or settings.

Mitigation: Store the key only in trusted local configuration, do not commit it to source control, and rotate it if exposure is suspected.

Risk: Generated route feasibility, distance, and travel-time analysis may be incomplete or outdated for real-world conditions.

Mitigation: Review the itinerary before acting on it and confirm critical travel details with an authoritative navigation or travel source.

## Reference(s):

- [ClawHub Travel Planner Skill Page](https://clawhub.ai/james-southendsolutions/skills/camino-travel-planner)
- [Camino API Key Activation](https://app.getcamino.ai/skills/activate)
- [Camino Journey API Endpoint](https://api.getcamino.ai/journey)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON route-planning response with feasibility, distance, travel time, route segments, and analysis fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires waypoint JSON with at least two stops; optional constraints include transport mode, time budget, and route preferences.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
