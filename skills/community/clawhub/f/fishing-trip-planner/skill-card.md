## Description:

AI fishing trip planning assistant that uses Gaode Map and QWeather APIs to generate route, weather, tide, scoring, and safety guidance in an HTML trip report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan fishing trips by collecting origin, destination, date, and travel mode, then generating route, weather, tide, scoring, and suggestion outputs. It is especially relevant for trips where local weather, coastal tide data, and travel logistics should be reviewed together before departure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores API keys, trip history, and reports locally, which can expose sensitive credentials or location data if files are shared or permissions are weak.

Mitigation: Use non-sensitive API keys, keep generated configuration and history private, and review local file permissions before sharing the workspace or reports.

Risk: Generated HTML reports may include API or location data that has not been fully contained or escaped.

Mitigation: Review generated HTML before opening or sharing it, especially when inputs or API responses could be manipulated.

Risk: The `--output` option can write reports to caller-selected paths.

Mitigation: Avoid existing, shared, or sensitive output paths and keep report generation in a dedicated directory.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/bettermen/fishing-trip-planner)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/fishing-trip-planner)
- [API configuration guide](references/api_guide.md)
- [Gaode Map API](https://lbs.amap.com/)
- [QWeather API](https://dev.qweather.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands that run a Python script and generate local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided API keys and may save local configuration, trip history, and HTML reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
