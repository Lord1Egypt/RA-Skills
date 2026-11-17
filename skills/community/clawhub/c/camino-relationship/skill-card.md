## Description:

Calculate spatial relationships between two points including distance, direction, travel time, and human-readable descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to calculate distance, direction, estimated travel times, and plain-language spatial descriptions between two latitude/longitude points through Camino's relationship API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends exact start and end coordinates to Camino's API.

Mitigation: Avoid sensitive home, workplace, medical, or regulated-location data unless Camino's data handling is acceptable for the use case.

Risk: The artifact's install examples are not version-pinned.

Mitigation: Use a pinned version or commit and install only the specific skill needed.

## Reference(s):

- [ClawHub Relationship skill page](https://clawhub.ai/james-southendsolutions/skills/camino-relationship)
- [Camino API activation](https://app.getcamino.ai/skills/activate)
- [Camino relationship API endpoint](https://api.getcamino.ai/relationship)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration]

**Output Format:** [JSON API response, with shell-command examples and configuration guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; sends supplied start and end coordinates to api.getcamino.ai.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
