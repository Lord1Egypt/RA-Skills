## Description: <br>
Queries Chinese city weather forecasts from weather.com.cn with optional JSON output and life-index guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodcoal](https://clawhub.ai/user/woodcoal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Chinese city weather questions, including current-day or seven-day forecasts, structured JSON output, and optional life-index advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to external weather providers and may reveal a user's requested location. <br>
Mitigation: Ask for location confirmation when a prompt is vague and avoid sending sensitive or unintended location details. <br>
Risk: Searched city names may be saved locally in citys.txt for future lookups. <br>
Mitigation: Review or clear the local city-code cache when lookup history should not persist. <br>
Risk: Weather data can be delayed or unavailable because the skill depends on network access to weather providers. <br>
Mitigation: Treat results as provider-supplied weather guidance and retry or use documented fallback providers when the primary source is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/woodcoal/china-weather-skill) <br>
- [weather.com.cn](https://www.weather.com.cn/) <br>
- [Referenced China Weather skill](https://clawhub.ai/hoopan007/weather-china) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text weather report or structured JSON forecast] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports city name input plus -json, -today, and -life options; may save newly discovered city codes in citys.txt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
