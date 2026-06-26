## Description: <br>
Provides a Portuguese daily dashboard for location, weather, forecasts, currency exchange rates, holidays, and contextual daily tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ExtAlisson3](https://clawhub.ai/user/ExtAlisson3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users invoke this skill to receive a concise Portuguese daily briefing with local conditions, Brazil-focused calendar context, currency quotes, and a fixed visual markdown layout. <br>

### Deployment Geography for Use: <br>
Brazil <br>

## Known Risks and Mitigations: <br>
Risk: Briefing generation contacts public services for weather, currency, and holiday data, which may reveal the requested city or approximate location. <br>
Mitigation: Invoke the skill intentionally with an explicit briefing command and adjust or omit location details when location disclosure is a concern. <br>
Risk: The broad alternate trigger "dia" could start the briefing unexpectedly. <br>
Mitigation: Prefer explicit commands such as "briefing diario" or "briefing" when configuring or invoking the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ExtAlisson3/briefing-diario) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=-19.9208&longitude=-43.9378&daily=uv_index_max,sunset,sunrise&hourly=precipitation_probability&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=auto) <br>
- [AwesomeAPI currency quote endpoint](https://economia.awesomeapi.com.br/json/last/USD-BRL,JPY-BRL,BTC-BRL,KRW-BRL,EUR-BRL) <br>
- [Nager.Date Brazil public holidays endpoint](https://date.nager.at/api/v3/PublicHolidays/2026/BR) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown code block with a fixed visual briefing layout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portuguese output with placeholders filled from public weather, exchange-rate, and holiday sources; friendly fallback text is used when a source is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
