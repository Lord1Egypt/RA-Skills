## Description: <br>
Track global city temperatures and analyze El Nino/La Nina (ENSO) phenomena with Imperial Modernity visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravenquasar](https://clawhub.ai/user/ravenquasar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and climate-data users use this skill to query current ENSO status, track hot-city weather data, and generate ENSO and temperature charts from public data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an OpenWeatherMap API key in a local config file. <br>
Mitigation: Keep config.json local, exclude it from version control, and rotate the API key if it is exposed. <br>
Risk: The skill contacts NOAA, OpenWeatherMap, and Berkeley Earth to retrieve weather and climate data. <br>
Mitigation: Install and run the skill only when this network access is acceptable for the environment. <br>
Risk: Custom --output values can write generated charts to user-selected file paths. <br>
Mitigation: Review output paths before running commands, especially when using custom --output values. <br>


## Reference(s): <br>
- [Enso Tracker on ClawHub](https://clawhub.ai/ravenquasar/enso-tracker) <br>
- [NOAA Climate Prediction Center ONI Data](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt) <br>
- [OpenWeatherMap API](https://openweathermap.org/api) <br>
- [Berkeley Earth Data](http://berkeleyearth.org/data/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands, CLI text output, and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write PNG charts to user-selected output paths and requires a local OpenWeatherMap API key for city weather queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
