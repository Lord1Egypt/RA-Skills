## Description: <br>
Dashboard Builder Free helps agents generate local static HTML dashboards from a user-provided data source, with supporting fetch scripts, configuration files, data snapshots, and basic visual QA guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and small teams use this skill to turn a described data source or monitoring need into a local dashboard folder with HTML, JSON configuration, data snapshots, and fetch scripts. It is best suited to single-source personal or small-team KPI dashboards rather than real-time streaming, multi-source aggregation, alerting, or team sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated fetch scripts may run shell commands or call external APIs with user credentials. <br>
Mitigation: Review generated fetch.sh before execution and keep API keys in environment variables or local environment files rather than hardcoding them. <br>
Risk: Dashboard previews or generated data files may expose sensitive data if served publicly. <br>
Mitigation: Bind local previews to 127.0.0.1, redact sensitive fields before writing data.json, and add authentication and access controls before any shared deployment. <br>
Risk: Generated dashboards can present incorrect, stale, or incomplete data when fetch scripts fail or the data source schema changes. <br>
Mitigation: Validate data.json, inspect browser console output, and complete visual QA before relying on or publishing the dashboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dashboard-builder-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with generated HTML, shell scripts, JSON configuration, data files, and local preview commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local dashboard artifacts such as index.html, fetch.sh, config.json, data.json, registry.json, and screenshot QA notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
