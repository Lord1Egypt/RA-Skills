## Description: <br>
Plan complete day trips, walking tours, and multi-stop itineraries with time budgets using Camino AI's journey planning and route optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to plan walking tours, day trips, and multi-stop itineraries with transport preferences and time budgets. The skill calls Camino's journey service with waypoint coordinates, stop purposes, and trip constraints, then returns route feasibility and optimization details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Waypoint coordinates, stop names, trip constraints, and route preferences are sent to Camino's service. <br>
Mitigation: Avoid sending sensitive home, workplace, medical, or private-trip details unless Camino's data handling is acceptable for the use case. <br>
Risk: The skill requires a Camino API key and shells out to curl. <br>
Mitigation: Store CAMINO_API_KEY in the agent environment rather than prompts or shared files, and review the command before execution. <br>
Risk: The release is part of a larger Camino companion suite. <br>
Mitigation: Install only camino-travel-planner unless the broader Camino location-intelligence skill set is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-travel-planner) <br>
- [Camino API key activation](https://app.getcamino.ai/skills/activate) <br>
- [Camino journey API endpoint](https://api.getcamino.ai/journey) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; sends waypoint coordinates, stop names, trip constraints, and route preferences to Camino.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
