## Description:

Find EV charging stations along a route or near a destination using Camino AI's location intelligence with OpenStreetMap data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find EV charging stations near coordinates, cities, highways, hotels, or other destinations through Camino AI location intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install instructions and all-companion-skills installation can introduce code outside this reviewed artifact.

Mitigation: Install only the intended camino-ev-charger version, prefer pinned versions or commit hashes, and review companion skills before installing them.

Risk: EV charger search requests can disclose the Camino API key and location details to Camino's API.

Mitigation: Use approved API keys, avoid submitting sensitive locations, and account for Camino API data handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-ev-charger)
- [Camino API activation](https://app.getcamino.ai/skills/activate)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; EV charger searches are sent to Camino's API.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
