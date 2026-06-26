## Description: <br>
Gets local weather and generates a humorous good-morning greeting or cheesy pickup line based on the conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrencheski](https://clawhub.ai/user/wrencheski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal morning assistant that checks the day's local weather and turns it into a light, weather-aware greeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookup may send the user's city to the configured weather service. <br>
Mitigation: Use only city information appropriate for the configured service and disclose when weather data is being requested. <br>
Risk: A broad or reused weather API key could increase exposure if it is mishandled. <br>
Mitigation: Configure a limited weather API key for this skill and rotate it if access is no longer needed. <br>
Risk: Network errors or invalid API credentials can prevent weather-aware output. <br>
Mitigation: Tell the user when weather data cannot be retrieved and use the documented generic morning greeting fallback. <br>


## Reference(s): <br>
- [Daily Greeting Bot ClawHub page](https://clawhub.ai/wrencheski/daily-greeting-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style weather summary and short greeting text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fallback greeting text when weather data is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
