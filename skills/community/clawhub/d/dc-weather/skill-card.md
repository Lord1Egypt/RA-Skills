## Description: <br>
Check Washington DC weather using Open-Meteo API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vital1188](https://clawhub.ai/user/vital1188) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to fetch and format current weather for Washington, DC without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the Open-Meteo weather API. <br>
Mitigation: Confirm the environment permits this API request before using the skill. <br>
Risk: The example commands depend on curl and jq being available locally. <br>
Mitigation: Install or verify curl and jq before relying on the generated weather command. <br>


## Reference(s): <br>
- [Open-Meteo forecast API endpoint](https://api.open-meteo.com/v1/forecast?latitude=38.9072&longitude=-77.0369&current_weather=true&temperature_unit=fahrenheit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and formatted weather text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Open-Meteo and local curl and jq binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
