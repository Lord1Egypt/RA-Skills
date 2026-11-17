## Description:

Austin CapMetro transit - real-time vehicle positions, next arrivals, service alerts, route info, and trip planning for buses and rail (MetroRail, MetroRapid, MetroBus). Use when the user asks about Austin public transit, bus schedules, train times, CapMetro alerts, or nearby stops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to answer Austin CapMetro transit questions, including next arrivals, live vehicle locations, service alerts, route details, nearby stops, and basic trip-planning support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a vulnerable protobuf parser dependency.

Mitigation: Update protobufjs to a patched current 8.x release before normal use and reinstall dependencies.

Risk: The skill refreshes GTFS static data by extracting a downloaded ZIP file into a local cache.

Mitigation: Validate ZIP entries before extraction and review the local cache path and file permissions before deployment.

Risk: The security guidance says the expected gtfs-realtime.proto file is missing.

Mitigation: Include the missing proto file or verify fallback behavior before relying on protobuf GTFS-RT feeds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brianleach/skills/capmetro-skill)
- [CapMetro Developer Tools](https://www.capmetro.org/developertools)
- [Texas Open Data Portal](https://data.texas.gov)
- [GTFS Reference](https://gtfs.org)
- [GTFS Realtime Reference](https://gtfs.org/realtime/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown/plain text responses with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-time transit arrivals, service alerts, vehicle positions, route and stop details, fare notes, and setup or refresh commands.]

## Skill Version(s):

1.0.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
