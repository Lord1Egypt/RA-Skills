## Description: <br>
免费天气技能免费版 helps personal users and developers query global weather through wttr.in and Open-Meteo without an API key, with text, JSON, PNG, shell-command, and scripting examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate weather lookup commands and code snippets for single-city current conditions and short forecasts through free public weather APIs. It is intended for command-line weather checks, scripting integration, development debugging, and terminal weather display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports a weather-query skill whose trigger and authority are broader than its stated purpose. <br>
Mitigation: Use the skill only for weather-related requests and review proposed commands before execution. <br>
Risk: The skill declares exec and write capabilities and includes optional examples that edit shell profile files. <br>
Mitigation: Review any alias or profile changes before applying them, and avoid granting write access beyond what the weather workflow requires. <br>
Risk: Location queries may be sent to wttr.in or Open-Meteo. <br>
Mitigation: Avoid submitting sensitive or private locations, and confirm external API use is acceptable for the deployment context. <br>
Risk: The artifact notes public-service rate limits and no SLA for the free weather APIs. <br>
Mitigation: Keep request volume modest, use the documented fallback service when needed, and do not rely on the skill for high-availability weather operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/free-weather-skill-tool-free) <br>
- [wttr.in](https://wttr.in) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, JSON examples, and weather API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather queries may call wttr.in or Open-Meteo; optional setup examples may modify shell profile files.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
