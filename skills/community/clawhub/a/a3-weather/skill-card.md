## Description:

Provides a concise OpenWeatherMap summary for daily briefings and weather forecasts for meeting times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rusheel080703](https://clawhub.ai/user/rusheel080703)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to add concise current and near-term weather to daily briefings, or forecast conditions around a meeting time. It can also return structured weather data for the next 24 hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send the selected location and OpenWeatherMap API key to OpenWeatherMap.

Mitigation: Use a key intended for OpenWeatherMap and avoid supplying sensitive meeting locations; use the configured default location when appropriate.

Risk: The security scan verdict is benign, but its coverage was partial and the evidence is incomplete.

Mitigation: Review the skill's environment and network access before installing, as the scan guidance recommends.

## Reference(s):

- [OpenWeatherMap API](https://openweathermap.org/api)
- [a3-weather on ClawHub](https://clawhub.ai/rusheel080703/skills/a3-weather)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text weather summary or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current conditions and the next 24 hours, or a forecast around a selected time within the five-day forecast window.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
