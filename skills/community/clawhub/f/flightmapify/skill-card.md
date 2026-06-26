## Description: <br>
Find cheapest flights and create interactive flight route maps with real-time flight search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudy2steiner](https://clawhub.ai/user/rudy2steiner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-planning agents use this skill to generate an interactive HTML flight map, search direct and connecting flights between cities, and inspect route, price, duration, and booking information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts local background servers and serves files from the OpenClaw workspace. <br>
Mitigation: Run it in a limited workspace, avoid important occupied ports, and stop spawned servers manually after use. <br>
Risk: The skill uses FlyAI credentials from environment variables or local configuration. <br>
Mitigation: Use a dedicated FlyAI key with limited scope and avoid sharing important or personal credentials with the skill environment. <br>
Risk: The server-resolved security verdict is suspicious because of broad local server, credential, and process-control behavior. <br>
Mitigation: Review and scan the skill before deployment, and install only when those behaviors match the intended use. <br>


## Reference(s): <br>
- [FlightMapify ClawHub release](https://clawhub.ai/rudy2steiner/flightmapify) <br>
- [FlyAI API key console](https://flyai.open.fliggy.com/console) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated interactive HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local HTML flight map and starts local background servers for map display and flight-search API access.] <br>

## Skill Version(s): <br>
1.4.6 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
