## Description: <br>
F1 CLI helps agents answer Formula 1 data questions by using the third-party f1 command-line tool backed by the OpenF1 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barronlroth](https://clawhub.ai/user/barronlroth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and F1-focused agents use this skill to retrieve and compare Formula 1 sessions, results, telemetry, pit stops, standings, weather, race-control events, team radio, tire stints, and related statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party f1 CLI and network-backed OpenF1 queries. <br>
Mitigation: Install and use it only when third-party CLI execution and F1 query parameters sent to the OpenF1-backed service are acceptable. <br>
Risk: Raw filters or free-form query values could include personal or sensitive data. <br>
Mitigation: Avoid entering personal or sensitive data in filters, driver/session lookups, or other free-form query values. <br>
Risk: Large telemetry or location queries can retrieve high-volume data even when client-side limits are used. <br>
Mitigation: Prefer server-side filters before applying client-side limits for telemetry and location queries. <br>
Risk: Position time-series data can be mistaken for final race classification. <br>
Mitigation: Use driver standings for final race results and treat positions output as session time-series data. <br>


## Reference(s): <br>
- [OpenF1 API](https://openf1.org) <br>
- [F1 CLI on ClawHub](https://clawhub.ai/barronlroth/f1-cli) <br>
- [Publisher profile](https://clawhub.ai/user/barronlroth) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or CSV command-output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the third-party f1 CLI, which queries OpenF1-backed services and can return table, JSON, or CSV data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
