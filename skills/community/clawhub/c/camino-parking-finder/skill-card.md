## Description:

Locate parking garages, lots, and street parking near your destination using Camino AI's location intelligence with AI-powered ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find parking garages, lots, and street parking near destinations or coordinates through Camino AI location intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parking searches, optional exact coordinates, and API-key-authenticated requests are sent to Camino's remote API.

Mitigation: Avoid submitting sensitive exact locations unless needed, use a scoped trusted API key, and review Camino's handling of submitted location data.

Risk: The broad companion-suite install can add many related skills beyond parking search.

Mitigation: Install the specific camino-parking-finder skill unless the full Camino location-intelligence suite is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-parking-finder)
- [Camino API activation](https://app.getcamino.ai/skills/activate)
- [Camino API endpoint](https://api.getcamino.ai/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; sends parking searches and optional coordinates to Camino API.]

## Skill Version(s):

2.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
