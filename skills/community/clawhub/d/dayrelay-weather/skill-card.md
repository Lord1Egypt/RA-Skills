## Description:

Fetch a compact, validated daily forecast for an explicitly supplied city coordinate and timezone, suitable for a scheduled personal briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aejin1211](https://clawhub.ai/user/aejin1211)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals can use the skill in a scheduled personal briefing to summarize today's forecast for a city they explicitly select, including high and low temperatures, precipitation probability, maximum wind, and a short condition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Open-Meteo and may use UTC when no timezone is supplied.

Mitigation: Use explicitly selected public city coordinates and supply the intended IANA timezone.

Risk: Security inspection was partial, with one component only partially inspected and a degraded tool-misuse analyzer.

Mitigation: Review the supplied skill files and network behavior before installation.

## Reference(s):

- [ClawHub dayrelay-weather release](https://clawhub.ai/aejin1211/skills/dayrelay-weather)
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
- [Open-Meteo data licence](https://open-meteo.com/en/licence)
- [Weather data by Open-Meteo](https://open-meteo.com/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON forecast data summarized as concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes date, timezone, units, provider attribution, and null values for unavailable measurements; output is for the explicitly selected location.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
