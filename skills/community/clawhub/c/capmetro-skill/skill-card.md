## Description: <br>
Austin CapMetro transit - real-time vehicle positions, next arrivals, service alerts, route info, and trip planning for buses and rail (MetroRail, MetroRapid, MetroBus). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer Austin CapMetro transit questions, including next arrivals, vehicle locations, service alerts, route details, nearby stops, and basic trip-planning support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a Node dependency before use. <br>
Mitigation: Review the package lock and install command before deployment, then install dependencies from the skill directory. <br>
Risk: The skill contacts public data.texas.gov feeds and stores schedule data under ~/.capmetro/gtfs/. <br>
Mitigation: Allow only the documented public feed access and confirm the local cache location is acceptable for the deployment environment. <br>
Risk: Alerts and trip-update features may depend on gtfs-realtime.proto being present in the installed copy. <br>
Mitigation: Verify the required proto file is included before relying on protobuf-backed real-time features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brianleach/capmetro-skill) <br>
- [CapMetro Developer Tools](https://www.capmetro.org/developertools) <br>
- [Texas Open Data Portal](https://data.texas.gov) <br>
- [GTFS Reference](https://gtfs.org) <br>
- [GTFS Realtime Reference](https://gtfs.org/realtime/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text transit summaries with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include arrival times, route names, service alerts, stop details, vehicle locations, and local setup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
