## Description: <br>
Evaluate any address for home buyers and renters. Get nearby schools, transit, grocery stores, parks, restaurants, and walkability using Camino AI's location intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate residential addresses or coordinates for nearby schools, transit, grocery stores, parks, restaurants, and walkability context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addresses or coordinates entered by the user are sent to Camino AI for processing. <br>
Mitigation: Use only location data appropriate for Camino AI and review applicable privacy or usage terms before entering sensitive addresses. <br>
Risk: The skill requires a CAMINO_API_KEY and may be subject to quota or billing terms. <br>
Mitigation: Store the key securely in the agent environment, use a key intended for this service, and monitor quota or billing usage. <br>
Risk: The artifact describes installing the broader Camino skill suite, which increases the installed surface area. <br>
Mitigation: Prefer the specific camino-real-estate install command unless the companion skills are intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-real-estate) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino query API](https://api.getcamino.ai/query) <br>
- [Camino context API](https://api.getcamino.ai/context) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; sends the provided address or coordinates to Camino AI.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
