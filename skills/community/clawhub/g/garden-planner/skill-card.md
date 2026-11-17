## Description:

Comprehensive garden planning - track plants, get planting recommendations, watering schedules, and frost alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local garden log, plan planting by USDA hardiness zone, track watering schedules, and check short-range frost risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather and ZIP-based frost checks send coordinates or location-derived data to Open-Meteo.

Mitigation: Use only the location precision needed for frost checks and avoid running weather commands when location sharing is not acceptable.

Risk: Plant records, watering schedules, notes, and configured coordinates are stored in a local garden JSON file.

Mitigation: Use the data-directory override for controlled storage and avoid putting sensitive personal details in garden notes.

Risk: Planting recommendations rely on average USDA zone and frost-date references, which may not reflect local microclimates.

Mitigation: Treat recommendations as planning guidance and compare them with local conditions before planting or frost-protection decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/garden-planner)
- [Planting Calendar by USDA Hardiness Zone](references/planting-calendar.md)
- [USDA Plant Hardiness Zones](references/zones.md)
- [Example garden data file](assets/garden.example.json)
- [USDA Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov/)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, local JSON data, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores garden records locally in a configurable data directory and can call Open-Meteo for weather and ZIP geocoding checks.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
