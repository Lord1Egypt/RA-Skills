## Description:

Search for gyms, yoga studios, swimming pools, and sports facilities using Camino AI's location intelligence with AI-powered ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find nearby gyms, yoga studios, swimming pools, and sports facilities by location or search query. It supports location-based fitness discovery with ranked JSON results from Camino AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fitness searches may send precise location data to the Camino API.

Mitigation: Avoid sending sensitive precise locations unless needed for the task.

Risk: The skill requires an API key for Camino requests.

Mitigation: Use a dedicated Camino API key and avoid sharing it in prompts, logs, or command output.

Risk: Mutable install commands can pull code that differs from the reviewed artifact.

Mitigation: Prefer a pinned release or reviewed commit, and install only camino-fitness-finder when the broader Camino suite is not needed.

## Reference(s):

- [Fitness Finder on ClawHub](https://clawhub.ai/james-southendsolutions/skills/camino-fitness-finder)
- [Camino AI skill activation](https://app.getcamino.ai/skills/activate)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown instructions with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq for the bundled shell workflow.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
