## Description: <br>
Looks up current weather, forecasts, alerts, and lifestyle indices for Chinese cities using city names or city codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libaoming](https://clawhub.ai/user/libaoming) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer weather questions for Chinese cities, including current conditions, tomorrow or weekly forecasts, alerts, and practical advice such as clothing or umbrella guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried city names are sent to external weather services such as wttr.in, and to QWeather when the optional provider is configured. <br>
Mitigation: Avoid sensitive private location details, and set QWEATHER_KEY only when intentionally using the optional weather provider. <br>
Risk: Recent current-weather results are briefly cached under /tmp. <br>
Mitigation: Treat /tmp/china-weather-cache as local query history and clear it when shared or sensitive environments require cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/libaoming/china-weather) <br>
- [QWeather Developer Portal](https://dev.qweather.com) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make network requests to wttr.in or QWeather and cache recent current-weather results in /tmp for 10 minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
