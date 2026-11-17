## Description:

Track global city temperatures and analyze El Niño/La Niña (ENSO) phenomena with Imperial Modernity visualization

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravenquasar](https://clawhub.ai/user/ravenquasar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and climate-data users can use this skill to fetch ENSO status and weather data, compare ONI periods, and generate publication-style charts for city heat rankings, temperature anomalies, ENSO timelines, and ENSO-to-heat correlation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an OpenWeatherMap API key in config.json with weak file-protection assumptions.

Mitigation: Keep the key outside the skill directory when possible, use a virtual environment, and restrict config.json to user-only permissions.

Risk: Correlation and anomaly charts can be misleading when real data is unavailable and simulated data is used.

Mitigation: Treat charts as unreliable whenever the tool reports simulated data, and verify conclusions against source datasets before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ravenquasar/skills/enso-tracker)
- [NOAA Climate Prediction Center ONI index](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Berkeley Earth data](http://berkeleyearth.org/data/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG chart files from the skill CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live NOAA, OpenWeatherMap, and Berkeley Earth data availability; some charting paths may fall back to simulated data when source data is unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
