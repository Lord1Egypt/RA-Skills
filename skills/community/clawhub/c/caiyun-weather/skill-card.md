## Description: <br>
Queries Caiyun Weather for realtime weather, air quality, hourly and weekly forecasts, recent history, and weather alerts by Chinese or English city name or coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather questions for supported cities using Caiyun Weather data, including forecasts, AQI, recent history, and alerts. It is most useful when the user has configured a Caiyun Weather API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Caiyun Weather API token and sends requested city names or coordinates to online weather services. <br>
Mitigation: Use only approved API tokens, avoid sensitive precise-location queries, and deploy only where sharing location queries with Caiyun Weather and OpenStreetMap Nominatim is acceptable. <br>
Risk: Weather, forecast, AQI, history, and alert results depend on third-party API availability, limits, and data freshness. <br>
Mitigation: Treat responses as informational, retry or verify when API calls fail, and use official or specialized sources for safety-critical, aviation, marine, or emergency decisions. <br>


## Reference(s): <br>
- [Caiyun Weather API Documentation](https://docs.caiyunapp.com/weather-api/) <br>
- [Caiyun Weather API Endpoint](https://api.caiyunapp.com/v2.6) <br>
- [OpenStreetMap Nominatim Search API](https://nominatim.openstreetmap.org/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/tjefferson/caiyun-weather) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text weather reports with concise Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAIYUN_WEATHER_API_TOKEN and may call Caiyun Weather and OpenStreetMap Nominatim over the network.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
