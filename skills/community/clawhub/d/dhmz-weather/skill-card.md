## Description:

Get Croatian weather data, forecasts, and alerts from DHMZ (meteo.hr) - no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[faleksic](https://clawhub.ai/user/faleksic)

### License/Terms of Use:

MIT

## Use Case:

Developers and Claude Code users use this skill to fetch Croatian current weather, forecasts, warnings, maritime, agricultural, and hydrological data from official DHMZ XML endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may infer a city from conversation context when no city is provided, which can create minor privacy and control concerns.

Mitigation: Provide the city explicitly, such as /dhmz-weather Zagreb, so the agent does not rely on conversation context.

## Reference(s):

- [DHMZ Weather on ClawHub](https://clawhub.ai/faleksic/skills/dhmz-weather)
- [DHMZ XML Data Products](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici)
- [DHMZ Official Website](https://meteo.hr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized weather data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl to retrieve XML data from public DHMZ endpoints; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
