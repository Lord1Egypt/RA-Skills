## Description:

查询指定城市或地区的天气预报信息，包括温度、天气状况、降水概率、风力风向等。支持实时天气和未来多日预报查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[congwupiece](https://clawhub.ai/user/congwupiece)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query current weather, multi-day forecasts, severe-weather alerts, and practical travel suggestions for a specified city or region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may naturally answer in Chinese and use Celsius-style weather reporting.

Mitigation: Ask the agent to adapt the response language and units when a different locale or unit system is needed.

Risk: Weather forecasts and alerts can affect travel and safety decisions.

Mitigation: For severe weather or high-impact plans, confirm critical details against an authoritative local weather source before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/congwupiece/skills/free-weather-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON plus a concise natural-language weather report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses location, days, and details inputs; normally reports Celsius-style weather data and may answer in Chinese unless the agent adapts language or units.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
