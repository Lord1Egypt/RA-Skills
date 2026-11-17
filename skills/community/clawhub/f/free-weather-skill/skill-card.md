## Description:

Get current weather and forecasts without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current weather, compact weather summaries, and forecasts from no-key weather services. It is useful when an agent needs quick human-readable weather output or fallback JSON weather data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather locations or coordinates may be sent to wttr.in or Open-Meteo.

Mitigation: Install only when that data sharing is acceptable, and avoid sending sensitive or unnecessary location detail.

Risk: The wttr.in examples use implicit protocol URLs and simple curl commands.

Mitigation: Prefer explicit https:// URLs and curl failure handling before using the commands in automated workflows.

Risk: The PNG example writes to /tmp/weather.png, which may be shared or predictable on some systems.

Mitigation: Use mktemp or a private directory for downloaded weather images.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and example service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. Weather lookups send requested locations or coordinates to external weather services.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
