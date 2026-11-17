## Description:

Smart garden irrigation reads soil sensors, checks weather, and decides when and how long to water each configured zone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowlderstudio](https://clawhub.ai/user/bowlderstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and garden operators use this skill to generate irrigation reports, review soil and weather conditions, and optionally run Tuya-connected watering valves for greenhouse or outdoor garden zones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real irrigation hardware automatically.

Mitigation: Use report-only mode or confirmation mode until valve IDs, countdown behavior, and zone limits are verified on the actual hardware.

Risk: Configured daily and minimum-interval safety limits may not be enforced consistently in all actuation paths.

Mitigation: Do not rely on those limits as the only protection; keep automation disabled or externally supervised until enforcement is reviewed.

Risk: Notifications can send irrigation reports to an external bot destination when enabled.

Mitigation: Disable report sending unless needed and verify bot account and target settings before use.

## Reference(s):

- [Garden Irrigation ClawHub Skill](https://clawhub.ai/bowlderstudio/skills/garden-irrigation)
- [tuya-cloud dependency](https://clawhub.ai/minshi-veyt/tuya-cloud)
- [Tuya API endpoint used by configuration](https://openapi.tuyaeu.com)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown irrigation report with plain-text command output and JSONL history files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open configured Tuya irrigation valves when automation is enabled; requires Tuya credentials, device IDs, zone configuration, and network access.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
