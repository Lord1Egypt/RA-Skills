## Description: <br>
Comprehensive beach surf conditions via mcporter MCP call for surf, waves, swim conditions, rip currents, or beach safety at beaches worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanfoglia](https://clawhub.ai/user/evanfoglia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve beach safety, surf, UV, wind, wave, and rip-current condition summaries or structured data for a named beach or coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Beach names or coordinates may be sent to public mapping and weather providers. <br>
Mitigation: Avoid using highly sensitive location queries when that sharing is a concern. <br>
Risk: Beach safety reports can be incomplete or unavailable when upstream public data sources do not provide local conditions. <br>
Mitigation: Use the report as situational guidance and follow local lifeguard, posted, or official emergency advisories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evanfoglia/beach-safety) <br>
- [NOAA National Weather Service API](https://api.weather.gov) <br>
- [Open-Meteo Marine API](https://marine-api.open-meteo.com/v1/marine) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [OpenStreetMap Nominatim Search](https://nominatim.openstreetmap.org/search) <br>
- [Photon Geocoder](https://photon.komoot.io/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Plain text safety reports or structured JSON returned by MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include beach coordinates, timestamps, safety scores, rip-current risk, UV index, wave, swell, wind, temperature, and recommendations.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
