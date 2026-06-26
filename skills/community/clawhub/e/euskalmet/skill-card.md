## Description: <br>
Tool for obtaining weather forecasts for the Basque Country through the Euskalmet agency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero-astro](https://clawhub.ai/user/zero-astro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to retrieve Euskalmet weather data for supported Basque Country locations and format the forecast as a concise Basque-language weather update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A setup helper can print part of the Euskalmet API private key to the terminal or logs. <br>
Mitigation: Review or remove the private-key prefix print in scripts/test_env.py before installation or execution. <br>
Risk: The skill uses Euskalmet credentials and contacts external Euskalmet/Euskadi endpoints. <br>
Mitigation: Use dedicated, revocable API credentials and keep the .env file private. <br>
Risk: Forecast and icon download scripts write files inside the skill directory. <br>
Mitigation: Run the skill in a controlled workspace and review generated forecast and image files before reusing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zero-astro/euskalmet) <br>
- [Publisher profile](https://clawhub.ai/user/zero-astro) <br>
- [Euskalmet](https://www.euskalmet.euskadi.eus/) <br>
- [Euskadi API endpoint](https://api.euskadi.eus/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like Basque-language weather summary with inline temperatures and forecast labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches forecast JSON from Euskalmet/Euskadi endpoints, writes forecast and icon files inside the skill directory, and can include an optional personalized greeting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
