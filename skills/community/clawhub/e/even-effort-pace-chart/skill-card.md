## Description:

Convert GPX, KML, or FIT routes into even-effort trail pace charts, or compare recorded FIT activities with checkpoint plans and segment times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yihouzenmeban](https://clawhub.ai/user/yihouzenmeban)

### License/Terms of Use:

MIT-0

## Use Case:

Trail runners and race planners use it to create checkpoint-based pace schedules from route files and compare recorded activities with race plans after an event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic forecasts send route midpoint locations to Open-Meteo before confirmation.

Mitigation: Use local files and manual weather for offline operation, or confirm before requesting forecasts.

Risk: Downloaded activities and exported reports may contain personal activity or location information.

Mitigation: Protect downloaded activities and reports, and provide a Garmin key only when requesting activity downloads.

Risk: Live integrations and optional dependency contents were not independently validated.

Mitigation: Review the relevant integration behavior and optional dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yihouzenmeban/skills/even-effort-pace-chart)
- [Project repository](https://github.com/yihouzenmeban/trail-running-pace)
- [Configuration reference](references/configuration.en.md)
- [Activity comparison guide](references/comparison.en.md)
- [Pacing model and limitations](references/model.en.md)
- [Ascent methods and selection rationale](references/ascent-options.en.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Configuration instructions]

**Output Format:** [SVG pace charts and comparisons; optional HTML, CSV, and JSON exports; JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkpoint-based pacing plans and optional recorded-activity comparisons; chart labels are Chinese.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
