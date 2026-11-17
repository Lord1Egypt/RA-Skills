## Description:

天气查询 / Weather query. 实时查询天气、气温、空气质量（AQI/PM2.5）、逐小时预报、一周天气预报、历史天气和天气预警，支持中文城市名（北京/上海/深圳等）直接查询。Real-time weather, temperature, AQI, hourly/weekly forecast, historical weather and alerts via Caiyun Weather API. Supports Chinese city names directly. Requires CAIYUN_WEATHER_API_TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to query real-time weather, air quality, hourly and weekly forecasts, recent historical weather, and weather alerts for cities or coordinates. It is most useful for China-focused weather queries and supports Chinese city names directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries send requested cities or coordinates to Caiyun Weather, and unresolved city names may be sent to OpenStreetMap for geocoding.

Mitigation: Use the skill only when sharing the queried location with those services is acceptable; prefer explicit coordinates for locations where geocoding disclosure should be controlled.

Risk: The skill requires a Caiyun Weather API token.

Mitigation: Provide the token through the CAIYUN_WEATHER_API_TOKEN environment variable and avoid placing it in prompts, logs, or checked-in files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjefferson/skills/caiyun-weather)
- [Caiyun Weather API documentation](https://docs.caiyunapp.com/weather-api/)
- [Caiyun Weather API endpoint](https://api.caiyunapp.com/v2.6)
- [OpenStreetMap Nominatim geocoding endpoint](https://nominatim.openstreetmap.org/search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text weather results and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and CAIYUN_WEATHER_API_TOKEN; unresolved city names may be geocoded through OpenStreetMap.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
