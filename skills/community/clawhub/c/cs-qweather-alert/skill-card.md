## Description: <br>
Queries QWeather for current weather, multi-day forecasts, and active weather alerts for a requested city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savior1987](https://clawhub.ai/user/savior1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer city-level weather questions, including current conditions, 3-30 day forecasts, and weather alert status from QWeather. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the configured QWeather API host and uses a JWT token supplied by argument or local token file. <br>
Mitigation: Use a dedicated QWeather token and verify that QWEATHER_API_HOST points to an official or trusted HTTPS QWeather endpoint. <br>
Risk: Weather queries may leave sensitive location traces in /tmp/cslog or scripts/data/location.json. <br>
Mitigation: Clear the log directory and city cache when queried locations should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/savior1987/cs-qweather-alert) <br>
- [QWeather Beijing weather page](https://www.qweather.com/weather/beijing-101010100.html) <br>
- [QWeather Shanghai weather page](https://www.qweather.com/weather/shanghai-101020100.html) <br>
- [QWeather Nanjing weather page](https://www.qweather.com/weather/nanjing-101190101.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text weather summaries with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured QWeather API host and JWT token; may write local logs and city-location cache.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
