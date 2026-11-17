## Description:

Queries real-time weather, multi-day forecasts, alerts, and lifestyle indices for supported Chinese cities using China Weather Network data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucelau1987cn](https://clawhub.ai/user/brucelau1987cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer China city weather questions, including current conditions, up to five days of forecast data, weather alerts, and lifestyle guidance.

### Deployment Geography for Use:

Global; weather coverage is limited to supported cities in China.

## Known Risks and Mitigations:

Risk: Weather data is requested over an unencrypted HTTP endpoint, so results could be observed or altered by someone controlling the network path.

Mitigation: Use results as advisory information, avoid relying on them alone for safety-critical weather decisions, and cross-check important decisions with trusted official sources.

## Reference(s):

- [City code reference](references/cities.json)
- [China Weather Network](http://www.weather.com.cn/)
- [Weather data endpoint](http://d1.weather.com.cn/weather_index/{code}.html)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text weather summary, or JSON when requested with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a city name and network access to d1.weather.com.cn; forecast output supports up to 5 days and optional lifestyle indices.]

## Skill Version(s):

1.1.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
