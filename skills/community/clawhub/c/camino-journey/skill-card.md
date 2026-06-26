## Description: <br>
Plan multi-waypoint journeys with route optimization, feasibility analysis, and time budget constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan or validate multi-stop trips, estimate travel time and distance, and assess whether an itinerary fits route and time-budget constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Waypoint and itinerary details are sent to Camino for route planning. <br>
Mitigation: Avoid submitting private home addresses, client locations, sensitive travel-security locations, or other location data that should not leave the local environment. <br>
Risk: The skill requires a sensitive CAMINO_API_KEY credential. <br>
Mitigation: Use a dedicated Camino API key stored in the agent environment, limit who can access it, and rotate or revoke it if exposed. <br>
Risk: Installing the entire companion suite expands the amount of third-party skill code in the environment. <br>
Mitigation: Prefer scoped ClawHub or specific-skill installation unless the full suite has been reviewed for the intended use. <br>


## Reference(s): <br>
- [ClawHub Journey Skill Page](https://clawhub.ai/james-southendsolutions/camino-journey) <br>
- [Camino API Key Activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino Journey API Endpoint](https://api.getcamino.ai/journey) <br>
- [x402 Payment Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands; script output is formatted JSON from the Camino journey API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and CAMINO_API_KEY; sends waypoint and constraint JSON to the Camino journey API.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
