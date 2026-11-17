## Description:

Queries the Amap (高德) Weather API for real-time conditions and 4-day forecasts for China locations using city names or adcodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyatt88](https://clawhub.ai/user/wyatt88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and format weather for Chinese cities, including current conditions and four-day forecasts through Amap's Web Service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An Amap API key can be exposed through command-line arguments, shell history, or logged full request URLs.

Mitigation: Set AMAP_API_KEY in the environment, avoid passing --key on shared systems, avoid logging request URLs that include the key, and rotate any key that may have been exposed.

## Reference(s):

- [Amap Weather API Reference](references/api-docs.md)
- [Amap Web Service](https://lbs.amap.com)
- [Amap weatherInfo endpoint](https://restapi.amap.com/v3/weather/weatherInfo)
- [Amap adcode download](https://lbs.amap.com/api/webservice/download)
- [ClawHub skill page](https://clawhub.ai/wyatt88/skills/amap-weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and optional JSON weather output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit formatted Chinese weather summaries or raw JSON from the Amap API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
