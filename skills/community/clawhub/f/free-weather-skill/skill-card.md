## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and general agent users use this skill to look up current weather, compact weather summaries, and forecasts from public weather services without managing API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries may disclose city names, airport codes, or coordinates to public weather services. <br>
Mitigation: Avoid querying sensitive or private locations when that disclosure is not acceptable. <br>
Risk: The skill depends on outbound access to wttr.in or Open-Meteo and on the local curl binary. <br>
Mitigation: Confirm curl is available and that outbound requests to the selected weather service are allowed in the deployment environment. <br>


## Reference(s): <br>
- [Weather on ClawHub](https://clawhub.ai/CodeKungfu/free-weather-skill) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo API documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and optional JSON weather responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public weather services; queried locations may be sent to wttr.in or Open-Meteo.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
