## Description: <br>
Get real-time Indonesian weather forecasts and earthquake data from BMKG, Indonesia's official meteorological agency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thommyid](https://clawhub.ai/user/thommyid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Indonesian weather, rainfall, temperature, wind, humidity, early-warning, and earthquake questions with BMKG public data. It also helps agents look up Indonesian administrative location codes and include BMKG attribution in user-facing responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may make outbound requests to BMKG public services. <br>
Mitigation: Install only where public BMKG network access is acceptable, and review agent network permissions before deployment. <br>
Risk: The optional location lookup helper may run local Python code and test BMKG API responses. <br>
Mitigation: Review the helper script before use and run it in an environment where outbound public API calls are permitted. <br>
Risk: Weather and earthquake data may be unavailable, delayed, or superseded by BMKG updates. <br>
Mitigation: Include BMKG attribution in responses and direct users to BMKG when the API does not respond or when critical decisions require confirmation. <br>


## Reference(s): <br>
- [BMKG Location Code Reference](references/kode-wilayah.md) <br>
- [Indonesian Administrative Region Dataset](references/wilayah.sql) <br>
- [BMKG Public Weather Site](https://cuaca.bmkg.go.id) <br>
- [BMKG Weather Forecast API](https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah}) <br>
- [BMKG Early Warning Feed](https://data.bmkg.go.id/peringatan-dini-cuaca/) <br>
- [BMKG Latest Earthquake Data](https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json) <br>
- [BMKG Recent Earthquakes Data](https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API endpoint examples, shell commands, and formatted weather or earthquake summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound requests to public BMKG endpoints; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
