## Description: <br>
Monitoring earthquake, weather, and tsunami data in Indonesia using BMKG official data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluemeda](https://clawhub.ai/user/bluemeda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and explain Indonesian earthquake, tsunami-potential, weather forecast, and severe weather warning data from official BMKG sources. <br>

### Deployment Geography for Use: <br>
Indonesia <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to BMKG government domains for live monitoring data. <br>
Mitigation: Install and run it only in environments where outbound requests to the documented BMKG domains are acceptable. <br>
Risk: Live earthquake, tsunami-potential, and severe weather data can change quickly and may be unavailable or delayed. <br>
Mitigation: Treat results as current BMKG data snapshots and verify urgent safety decisions against official BMKG channels. <br>


## Reference(s): <br>
- [Seismology Reference](references/seismology.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bluemeda/bmkg-monitor) <br>
- [BMKG Earthquake Data](https://data.bmkg.go.id/DataMKG/TEWS/) <br>
- [BMKG Weather Forecast API](https://api.bmkg.go.id/publik/prakiraan-cuaca) <br>
- [BMKG Weather Warnings](https://www.bmkg.go.id/alerts/nowcast/id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests fetch live public BMKG data; command output may include earthquake details, weather forecasts, warnings, shakemap URLs, or raw JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
