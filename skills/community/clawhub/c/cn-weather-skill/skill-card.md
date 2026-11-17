## Description:

Queries current weather for mainland China cities using China Meteorological Administration station lookup and current-weather endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fy39913](https://clawhub.ai/user/fy39913)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about current weather, temperature, humidity, wind, visibility, forecasts, and lightweight travel or clothing advice for mainland China cities.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Shell-based examples can be unsafe if a user-provided city name is inserted directly into a command or JSON body.

Mitigation: Validate city names, safely serialize JSON request bodies, and prefer a structured HTTP client over direct shell interpolation.

Risk: The skill is narrowly scoped to mainland China weather and may not return appropriate results for unsupported regions.

Mitigation: Invoke it only for mainland China weather requests; for Hong Kong, Macau, Taiwan, or international cities, state that the skill is unsupported and use another source.

Risk: Incorrect or unexpected station IDs could lead to wrong weather results.

Mitigation: Validate returned station IDs and choose the best city match before querying current-weather data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fy39913/skills/cn-weather-skill)
- [China Meteorological Administration station lookup endpoint](https://data.cma.cn/kbweb/home/getStationID)
- [China Meteorological Administration current weather endpoint](https://weather.cma.cn/api/now/<station-id>)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown weather summary with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a human-facing current-weather summary and may include brief travel or clothing advice when supported by returned weather data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
