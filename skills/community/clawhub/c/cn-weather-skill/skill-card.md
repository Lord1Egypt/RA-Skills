## Description: <br>
Queries real-time weather for China mainland cities by resolving a city name to a CMA station ID and then fetching current conditions from CMA weather services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fy39913](https://clawhub.ai/user/fy39913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for current weather, temperature, humidity, wind, visibility, or short travel and clothing advice for a China mainland city. <br>

### Deployment Geography for Use: <br>
Global; weather lookups are limited to China mainland cities. <br>

## Known Risks and Mitigations: <br>
Risk: City names from weather queries are sent to CMA weather services. <br>
Mitigation: Avoid unusually precise or sensitive location details when that information should not be shared externally. <br>
Risk: Weather results depend on CMA endpoint availability and coverage for China mainland cities. <br>
Mitigation: Tell users when a city is unsupported or weather data cannot be fetched, and suggest retrying later or using a nearby supported city. <br>


## Reference(s): <br>
- [CMA station lookup endpoint](https://data.cma.cn/kbweb/home/getStationID) <br>
- [CMA current weather endpoint example](https://weather.cma.cn/api/now/58349) <br>
- [ClawHub skill page](https://clawhub.ai/fy39913/cn-weather-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown weather report with current conditions and optional short travel or clothing advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses city-name input, skips missing weather fields, and reports lookup or API failures without requiring credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
