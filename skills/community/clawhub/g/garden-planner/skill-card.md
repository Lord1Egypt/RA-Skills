## Description: <br>
Comprehensive garden planning: track plants, get planting recommendations, watering schedules, and frost alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and gardening-focused agents use this skill to track plants, watering schedules, planting windows, harvest readiness, and frost alerts for a local garden. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update a local garden.json file containing plant, watering, and location records. <br>
Mitigation: Use --data-dir to store the garden file in an intended location and review the file before sharing or committing it. <br>
Risk: Weather checks can send ZIP code or latitude/longitude to Open-Meteo. <br>
Mitigation: Run weather checks only when sharing that location data with Open-Meteo is acceptable. <br>
Risk: Planting and frost guidance depends on reference calendars, zone estimates, forecast data, and local microclimates. <br>
Mitigation: Treat recommendations as planning support and confirm time-sensitive garden actions against local observations or trusted local sources. <br>


## Reference(s): <br>
- [Garden Planner skill instructions](SKILL.md) <br>
- [Planting Calendar by USDA Hardiness Zone](references/planting-calendar.md) <br>
- [USDA Plant Hardiness Zones](references/zones.md) <br>
- [Example garden data file](assets/garden.example.json) <br>
- [USDA Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov/) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local garden.json file and may query Open-Meteo when weather checks are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
