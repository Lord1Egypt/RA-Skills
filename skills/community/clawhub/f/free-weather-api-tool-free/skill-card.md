## Description: <br>
Helps an agent query city weather, up to seven-day forecasts, air quality, severe-weather alerts, and practical travel or clothing suggestions for individual users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current weather, short forecasts, air quality, severe-weather alerts, and practical travel or clothing advice for a single city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan marked the release suspicious because the instructions are broader than the weather-helper purpose and request exec/write authority. <br>
Mitigation: Limit activation to weather, forecast, air-quality, alert, and travel-weather requests, and review commands before execution. <br>
Risk: Weather lookups send queried locations to network weather APIs. <br>
Mitigation: Use only for locations the user is comfortable sharing with external weather services. <br>
Risk: The artifact includes examples that can create local cache or configuration files. <br>
Mitigation: Grant write access only when local cache or default-location configuration is desired, and review file paths before writing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thcjp/skills/free-weather-api-tool-free) <br>
- [wttr.in weather API](https://wttr.in/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with text or JSON weather reports and optional bash or Python snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries public weather APIs and may create local cache or configuration files when the agent follows the examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
