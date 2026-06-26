## Description: <br>
Get comprehensive context about a location including nearby places, area description, and optional weather. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request location context for trip planning, meeting locations, local recommendations, and weather-aware planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise coordinates and request context are sent to Camino's third-party API. <br>
Mitigation: Use only the fields needed for the request, avoid private notes or sensitive locations, and confirm Camino's API and data handling practices are acceptable before use. <br>
Risk: The skill requires CAMINO_API_KEY, a sensitive credential. <br>
Mitigation: Store the key in the agent environment, do not include it in prompts or files, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-context) <br>
- [Camino API activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino Context API endpoint](https://api.getcamino.ai/context) <br>
- [x402 payment protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON API response printed to stdout, with Markdown documentation and shell examples in the skill artifact.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and the CAMINO_API_KEY environment variable.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
