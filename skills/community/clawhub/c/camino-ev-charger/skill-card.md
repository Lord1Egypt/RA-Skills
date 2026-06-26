## Description: <br>
Find EV charging stations along a route or near a destination using Camino AI's location intelligence with OpenStreetMap data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find EV charging stations near coordinates, cities, destinations, or route-planning waypoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EV charger searches may send coordinates, destination details, and related location context to Camino AI. <br>
Mitigation: Share only the location details needed for the task and review the query before executing the skill. <br>
Risk: The skill requires a Camino API key and may expose it if settings files or shell environments are shared carelessly. <br>
Mitigation: Use a dedicated Camino API key and avoid sharing or committing settings files that contain CAMINO_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/camino-ev-charger) <br>
- [Camino API activation](https://app.getcamino.ai/skills/activate) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON API results with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAMINO_API_KEY and the curl and jq command-line tools.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
