## Description:

Fornece um dashboard visual para informações do dia a dia como localização, clima, economia, previsão do tempo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extalisson3](https://clawhub.ai/user/extalisson3)

### License/Terms of Use:


## Use Case:

External users invoke this skill for a Brazil-focused Portuguese daily briefing that summarizes local weather, UV guidance, sunrise and sunset, exchange rates, holiday status, and a contextual daily tip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact public weather, exchange-rate, holiday, and time data services when preparing the briefing.

Mitigation: Use it only when a Brazil-focused daily briefing is desired and review network access expectations before deployment.

Risk: Generic trigger words such as dia could invoke the skill unintentionally.

Mitigation: Prefer explicit invocation phrases such as briefing diario or briefing in agent routing configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extalisson3/skills/briefing-diario)
- [Open-Meteo forecast API endpoint used by the skill](https://api.open-meteo.com/v1/forecast?latitude=-19.9208&longitude=-43.9378&daily=uv_index_max,sunset,sunrise&hourly=precipitation_probability&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=auto)
- [AwesomeAPI exchange-rate endpoint used by the skill](https://economia.awesomeapi.com.br/json/last/USD-BRL,JPY-BRL,BTC-BRL,KRW-BRL,EUR-BRL)
- [Nager public holidays endpoint used by the skill](https://date.nager.at/api/v3/PublicHolidays/2026/BR)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown code block containing a fixed-width Portuguese daily briefing dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes weather, UV, sunrise and sunset, exchange rates, holiday status, and a contextual tip; uses friendly fallback messages if a public data source fails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
