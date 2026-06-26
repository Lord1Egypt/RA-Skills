## Description: <br>
Track Air France flights using the Air France-KLM Open Data APIs (Flight Status) when the user gives a flight number/date and wants monitoring, alerts, previous-flight chain analysis, aircraft tail number context, cabin recency, Wi-Fi hints, or polling guidance within API rate limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iclems](https://clawhub.ai/user/iclems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers, travel operations staff, and developers use this skill to query and monitor Air France flight status, schedule changes, gates, terminals, aircraft assignments, cabin and Wi-Fi hints, and previous-flight delay risk. It helps set up one-off checks or schedule-aware polling with compact change alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AFKL API credentials may be exposed if environment variables or credential files are shared or stored with broad filesystem permissions. <br>
Mitigation: Use a dedicated AFKL API key, prefer environment variables or a private explicit state directory, and protect credential files with restrictive permissions. <br>
Risk: Local state and cache files can retain watched flight details and aircraft information after monitoring is no longer needed. <br>
Mitigation: Use a private state directory and delete watcher state, caches, and related cron entries after the flight-monitoring window ends. <br>
Risk: Polling too frequently can exceed AFKL API rate limits or daily quotas. <br>
Mitigation: Use the schedule-aware watcher defaults and keep calls at or below the documented one-request-per-second pace. <br>


## Reference(s): <br>
- [Air France-KLM Developer Portal](https://developer.airfranceklm.com) <br>
- [AFKL Flight Status fields to watch](references/fields.md) <br>
- [Planespotters public aircraft photo API](https://api.planespotters.net/pub/photos/reg/{reg}) <br>
- [ClawHub skill page](https://clawhub.ai/iclems/airfrance-afkl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or plain-text flight status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The watcher emits no output when nothing changes and emits compact, ready-to-send alerts when meaningful flight fields change.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
