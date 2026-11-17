## Description:

获取全球城市天气信息和预报。使用场景包括查询当前天气、未来7天预报、空气质量、穿衣建议等。适用于用户问天气、温度、预报等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmu14641](https://clawhub.ai/user/anmu14641)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language weather assistant to get current weather, seven-day forecasts, air quality details, clothing suggestions, travel reminders, and multi-city weather comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries may be sent to public weather services.

Mitigation: Avoid entering sensitive or unnecessarily precise locations when approximate city-level weather is sufficient.

Risk: Weather API availability and small-city coverage may be inconsistent.

Mitigation: Use the alternate data source when one provider fails and verify important forecasts with an official meteorological source.

Risk: Forecast accuracy decreases over longer time horizons and extreme weather may require authoritative alerts.

Mitigation: Treat longer-range forecasts and safety-critical weather decisions as advisory and confirm severe-weather conditions through official warnings.

Risk: The skill does not clearly define non-weather activation boundaries or multilingual behavior.

Mitigation: Limit use to weather-related requests and review outputs when prompts ask for unrelated tasks or languages outside the skill's stated Chinese-language use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmu14641/skills/anmu-weather)
- [Publisher profile](https://clawhub.ai/user/anmu14641)
- [wttr.in weather data source](https://wttr.in)
- [Open-Meteo weather data source](https://open-meteo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese-language weather reports and recommendation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current conditions, forecast lists, air quality, wind, humidity, sunrise and sunset details, clothing advice, travel reminders, and multi-city comparisons.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
