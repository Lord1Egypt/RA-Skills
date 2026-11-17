## Description:

Analyzes uploaded fishing-spot photos with location, weather, terrain, and seasonal fish patterns to produce a fishing report with scoring and gear recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhanchao883](https://clawhub.ai/user/wangzhanchao883)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate fishing locations from photos and location context, combining weather, visible terrain, seasonal fish patterns, and safety reminders into a practical outing report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded photos may contain precise EXIF GPS coordinates that the skill can use for weather lookup without clear consent.

Mitigation: Ask before reading EXIF GPS, explain that coordinates may be sent to Open-Meteo, and allow city-level location instead of exact coordinates.

Risk: Fishing recommendations may be unsafe or inappropriate if applied near hazardous terrain, restricted waters, or protected areas.

Mitigation: Preserve warnings for steep banks, storms, prohibited methods, posted no-fishing signs, protected areas, and local fishing restrictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhanchao883/skills/fishing-spot-analyzer)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m,precipitation&timezone=auto&forecast_days=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with scoring tables and recommendation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use exact photo GPS coordinates for weather lookup when EXIF data is available; falls back to city-level or seasonal analysis when location or weather data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
