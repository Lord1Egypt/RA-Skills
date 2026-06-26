## Description: <br>
Find 24-hour businesses, well-lit public areas, transit stations, police stations, and hospitals near any location for late night safety awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, developers, and agents use this skill to query nearby late-night safety resources around provided coordinates, including open businesses, transit, police stations, and hospitals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send user-provided coordinates and the Camino API key to Camino's API. <br>
Mitigation: Use only locations appropriate to share with the API provider and avoid highly sensitive exact coordinates when that privacy tradeoff is not acceptable. <br>
Risk: The skill requires a sensitive CAMINO_API_KEY environment variable. <br>
Mitigation: Store the key in the agent environment or secret manager, do not paste it into prompts, and rotate it if it is exposed. <br>
Risk: The artifact mentions paid x402 endpoints for clients that support HTTP 402 payments. <br>
Mitigation: Use the included API-key path unless paid requests are explicitly intended and spending controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-safety-checker) <br>
- [Camino API activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino context API endpoint](https://api.getcamino.ai/context) <br>
- [x402 payment protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON response from the Camino context API, with setup and usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, CAMINO_API_KEY, and user-provided latitude/longitude coordinates.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
