## Description: <br>
Route planning for Berlin public transport (BVG) using the v6.bvg.transport.rest API, including route suggestions, live next-departure information, arrive-by or depart-at planning, step-by-step directions, and refresh tokens for live updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaysonsantos](https://clawhub.ai/user/jaysonsantos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan Berlin public-transport journeys, check near-term departures, and produce concise step-by-step route options with transfer, walking, departure, and arrival details. <br>

### Deployment Geography for Use: <br>
Global use; route coverage is Berlin public transport. <br>

## Known Risks and Mitigations: <br>
Risk: Route-planning requests may send exact origin, destination, and timing details to v6.bvg.transport.rest. <br>
Mitigation: Avoid entering highly sensitive home, work, appointment, or other exact locations when that privacy exposure matters. <br>
Risk: The helper script requires local command-line dependencies when run directly. <br>
Mitigation: Confirm python3, curl, and jq are available and review the command before executing it. <br>


## Reference(s): <br>
- [v6.bvg.transport.rest API](https://v6.bvg.transport.rest/api.html) <br>
- [API.md](references/API.md) <br>
- [ClawHub skill page](https://clawhub.ai/jaysonsantos/bvg-route) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown route summaries with optional machine-friendly JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include journey refresh tokens, route legs, stop IDs, transfer counts, walking distances, and realtime departure or arrival times.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
