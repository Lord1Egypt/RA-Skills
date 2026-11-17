## Description:

Weather and forecasts via free services (wttr.in and Open-Meteo), with multi-city comparison, 7-day planning, and trading-hub weather checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current weather, compare forecasts across cities, plan around weekly weather, and check weather context for financial hubs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City and hub names are sent to third-party weather services and can reveal location interests or travel plans.

Mitigation: Use only city or hub names you are comfortable sharing with wttr.in and Open-Meteo, and avoid sensitive travel or location queries where disclosure would be a concern.

Risk: A bundled premium trading-weather client can use a spending-capable API key and may incur per-call charges.

Mitigation: Do not set X402_API_KEY or X402_BASE unless the paid integration is intentional, the endpoint is trusted, and the user accepts the charges.

Risk: The manifest and documentation emphasize free weather tools while the artifact includes a premium client.

Mitigation: Review the skill before installation and align the manifest and documentation with the bundled premium client or remove that client.

## Reference(s):

- [ClawWeather Pro on ClawHub](https://clawhub.ai/northcap-group/skills/clawweather-pro)
- [wttr.in weather service](https://wttr.in)
- [Open-Meteo forecast API](https://api.open-meteo.com)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown tables, plain text summaries, JSON from the premium client, and example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed weather results depend on third-party service availability and the city or hub names supplied by the user.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
