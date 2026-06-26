## Description: <br>
Manage Earl's TV dashboard (VisuoSpatial Sketchpad) by waking the display, restarting the local server, launching the kiosk browser, and updating mood, house tasks, hot takes, sketchpad doodles, and weather. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[recozers](https://clawhub.ai/user/recozers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and household operators use this skill to manage a local living-room TV dashboard, update its state through helper scripts or Python API calls, and recover the display when it is stale or sleeping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household notes, room state, patterns, and location can persist on disk in earl_mind.json. <br>
Mitigation: Avoid secrets in earl_mind.json, use approximate weather coordinates, or disable weather when location privacy matters. <br>
Risk: Dashboard data may be served through an unauthenticated local HTTP server. <br>
Mitigation: Bind the HTTP server to 127.0.0.1 or protect it with a firewall before use. <br>
Risk: Force-kill and clear/remove operations can stop processes or remove dashboard content. <br>
Mitigation: Confirm target processes and content before running force-kill, clear, or remove commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/recozers/earl-display-control) <br>
- [Project homepage from metadata](https://github.com/recozers/earl-display-control) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local server, kiosk browser, and JSON state update commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
