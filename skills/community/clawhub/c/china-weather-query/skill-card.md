## Description: <br>
Queries real-time weather, multi-day forecasts, air quality, alerts, and lifestyle indices for Chinese cities using China Weather Network data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucelau1987cn](https://clawhub.ai/user/brucelau1987cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather-related questions for Chinese cities, including current conditions, short forecasts, air quality, alerts, and practical travel or clothing advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound weather queries to weather.com.cn for requested cities. <br>
Mitigation: Use it only when that disclosed network access is acceptable and restrict egress to the weather service where containment is required. <br>
Risk: The script can look for city reference data in extra OpenClaw workspace fallback paths. <br>
Mitigation: Run it with file access limited to the bundled references/cities.json unless local fallback paths are intentionally needed. <br>
Risk: Weather, alert, and lifestyle-index results depend on the availability and freshness of the external weather service. <br>
Mitigation: Treat outputs as informational and verify critical safety, travel, or operational decisions against authoritative weather warnings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucelau1987cn/china-weather-query) <br>
- [City Code Reference](references/cities.json) <br>
- [China Weather Network](http://www.weather.com.cn/) <br>
- [China Weather Network Weather Endpoint](http://d1.weather.com.cn/weather_index/{code}.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text weather summary or JSON when requested; agent guidance may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to d1.weather.com.cn; supports city name, --days up to 5, --detail, and --json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
