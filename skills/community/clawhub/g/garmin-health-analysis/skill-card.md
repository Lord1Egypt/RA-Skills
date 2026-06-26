## Description: <br>
Lets agents answer natural-language questions about Garmin Connect health, recovery, sleep, activity, and route data while fetching metrics, downloading FIT/GPX files, querying point-in-activity details, and generating interactive health dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eversonl](https://clawhub.ai/user/eversonl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query Garmin Connect health, recovery, sleep, activity, and route data, then produce concise analysis, JSON data, shell commands, downloaded activity files, and interactive dashboard charts. It is suited to automated health monitoring, scheduled reports, proactive check-ins, and user-directed Garmin data exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Garmin account and can process sensitive health, activity, and route data. <br>
Mitigation: Install only when that access is acceptable, keep exported files private, and delete FIT, GPX, TCX, and chart outputs when they are no longer needed. <br>
Risk: Garmin credentials and session tokens can be exposed if stored or passed insecurely. <br>
Mitigation: Prefer environment or platform-managed secrets, avoid passing passwords on the command line, and protect the local token directory. <br>
Risk: Generated health analysis may be mistaken for medical advice. <br>
Mitigation: Use the outputs as informational trend analysis and include the documented disclaimer that the analysis is not medical advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eversonl/garmin-health-analysis) <br>
- [Garmin Connect API Reference (Unofficial)](references/api.md) <br>
- [Health Data Analysis Guide - Garmin Edition](references/health_analysis.md) <br>
- [Extended Garmin Capabilities](references/extended_capabilities.md) <br>
- [MCP Server for Standard Claude Desktop](references/mcp_setup.md) <br>
- [python-garminconnect library](https://github.com/cyberjunky/python-garminconnect) <br>
- [Garmin Connect](https://connect.garmin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON data from Garmin scripts, downloadable FIT/GPX/TCX files, and generated HTML charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May access sensitive Garmin account, health, activity, and route data; users should treat outputs and exported files as private.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
