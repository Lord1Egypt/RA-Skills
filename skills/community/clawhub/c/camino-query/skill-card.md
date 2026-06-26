## Description: <br>
Search for places using natural language with Camino AI's location intelligence API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search for restaurants, shops, landmarks, and other points of interest through Camino's location intelligence API. It supports natural-language place queries, optional coordinates and radius, ranking, pagination, historical or OSM-ID searches, and optional human-readable answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place searches, optional coordinates, and the Camino API key are sent to Camino. <br>
Mitigation: Use a dedicated revocable API key and avoid submitting sensitive home, work, or travel-intent queries unless they are necessary. <br>
Risk: The documentation advertises a companion suite, which increases the amount of code and behavior installed. <br>
Mitigation: Prefer the specific ClawHub or single-skill install command unless the full companion suite has been reviewed. <br>
Risk: The release is tagged with crypto and purchase-related capabilities because Camino describes optional x402 paid endpoints. <br>
Mitigation: Use the bundled API-key script for this skill, and confirm spending controls before using any separate x402-capable client path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-query) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino API](https://api.getcamino.ai/query) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [JSON responses from the Camino API, with optional human-readable answer text when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and the CAMINO_API_KEY environment variable for the bundled script.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
