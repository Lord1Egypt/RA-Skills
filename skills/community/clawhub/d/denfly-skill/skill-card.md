## Description:

Get current weather and forecasts without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denfly618](https://clawhub.ai/user/denfly618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent produce quick weather lookup commands and guidance for current conditions, forecasts, units, and programmatic JSON weather queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups disclose the requested city, airport code, or coordinates to external weather services along with normal network metadata such as IP address.

Mitigation: Use only locations appropriate to share with wttr.in or Open-Meteo, and avoid submitting sensitive coordinates or private place names.

Risk: The skill relies on network calls to third-party weather APIs, so results depend on those services being reachable and accurate.

Mitigation: Review API responses before acting on them and use the Open-Meteo fallback when wttr.in is unavailable or unsuitable.

## Reference(s):

- [wttr.in Help](https://wttr.in/:help)
- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs)
- [Open-Meteo Forecast API Example](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and occasional JSON API output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands for wttr.in or Open-Meteo and may describe PNG or JSON weather outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
