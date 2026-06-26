## Description: <br>
Fetch aviation weather data (METAR, TAF, PIREPs) from aviationweather.gov. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimitryvin](https://clawhub.ai/user/dimitryvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Pilots, flight planners, and aviation-focused agents use this skill to retrieve METAR observations, TAF forecasts, and nearby PIREPs for airport weather checks and briefing support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aviation weather can be incomplete, stale, or unsuitable as the sole basis for flight-critical decisions. <br>
Mitigation: Verify flight-critical weather through official aviation briefing channels before operational use. <br>
Risk: Airport identifiers or PIREP coordinates are sent to aviationweather.gov during lookups. <br>
Mitigation: Use only if sharing those lookup parameters with aviationweather.gov is acceptable. <br>


## Reference(s): <br>
- [AviationWeather.gov API](https://aviationweather.gov/api/data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown text or raw JSON from aviationweather.gov] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ICAO station identifiers for METAR and TAF lookups, and latitude, longitude, and radius for PIREP searches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
