## Description:

Route-aware weather forecasts for alpine climbs. Terrain-adjusted timing, multi-day camp-to-summit itineraries, three-source verification, descent conditions, and pace calibration that learns your speed over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundiraman](https://clawhub.ai/user/sundiraman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and climbing-focused agents use this skill to turn route names, GPX tracks, or simple elevation profiles into route-aware alpine weather forecasts with timing, confidence, and source verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted GPX file could fake or hide parts of forecast output through waypoint names.

Mitigation: Review before processing GPX files from untrusted sources and sanitize waypoint names before terminal or JSON output.

Risk: Long-range or single-source weather forecasts can be low confidence for alpine decision-making.

Mitigation: Show the forecast confidence level, cross-check available sources, and recommend checking again closer to the climb date for low-confidence forecasts.

Risk: Mountain-Forecast.com verification depends on scraped HTML that may break if the site layout changes.

Mitigation: Treat missing or failed Mountain-Forecast verification as degraded confidence and rely on available Open-Meteo or NOAA/NWS data where appropriate.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [NOAA/NWS API](https://api.weather.gov)
- [Mountain-Forecast.com](https://www.mountain-forecast.com)
- [GPX 1.1 namespace](http://www.topografix.com/GPX/1/1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style forecast summaries with terminal output and optional JSON forecast data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route timing, confidence level, ascent and descent conditions, weather warnings, and source verification where available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
