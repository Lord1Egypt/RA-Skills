## Description: <br>
Weather Plus helps agents answer weather questions with current conditions, seven-day forecasts, air quality, clothing advice, and multi-city comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmu14641](https://clawhub.ai/user/anmu14641) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather, temperature, forecast, air quality, clothing, travel, and multi-city comparison questions. It is intended for concise Chinese weather reports backed by wttr.in or Open-Meteo data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may send city, travel, or location intent to third-party weather services. <br>
Mitigation: Avoid entering sensitive private travel plans or precise locations unless sharing that information with wttr.in or Open-Meteo is acceptable. <br>
Risk: Forecast accuracy decreases over longer time horizons and extreme weather may require authoritative alerts. <br>
Mitigation: Use official meteorological warnings for safety-critical or extreme-weather decisions. <br>
Risk: Some locations may be unavailable or unreliable through wttr.in. <br>
Mitigation: Use Open-Meteo as a fallback where possible and treat missing small-city results as a data-source limitation. <br>


## Reference(s): <br>
- [Weather Plus on ClawHub](https://clawhub.ai/anmu14641/anmu-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Chinese Markdown weather reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact wttr.in or Open-Meteo for weather data; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
