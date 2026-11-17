## Description:

Check Washington DC weather using Open-Meteo API. Use when user asks about DC weather, current conditions, or needs a weather report for Washington DC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vital1188](https://clawhub.ai/user/vital1188)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch and format current weather conditions for Washington, DC from Open-Meteo without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes a network request to Open-Meteo for Washington, DC weather.

Mitigation: Review network access expectations before installation and execution; evidence.security reports no private local data access or lasting system changes.

## Reference(s):

- [DC Weather ClawHub skill page](https://clawhub.ai/vital1188/skills/dc-weather)
- [Open-Meteo forecast API request](https://api.open-meteo.com/v1/forecast?latitude=38.9072&longitude=-77.0369&current_weather=true&temperature_unit=fahrenheit)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and formatted weather text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a public Open-Meteo network request for Washington, DC coordinates and requires curl and jq for the provided command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
