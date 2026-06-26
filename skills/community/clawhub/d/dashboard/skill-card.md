## Description: <br>
Build custom dashboards from any data source with local hosting and visual QA loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and business users use this skill to create local static dashboards backed by user-selected APIs, files, or services while keeping credential setup and fetch execution under their control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboards and fetch scripts may touch sensitive APIs or local data when configured that way. <br>
Mitigation: Review every generated fetch script before running it, keep credentials in environment variables rather than files, and prefer read-only API keys. <br>
Risk: Dashboard data may expose sensitive or personal information. <br>
Mitigation: Avoid unnecessary PII in displayed data and protect the ~/dashboard directory. <br>
Risk: A dashboard exposed beyond localhost can become accessible to unintended users. <br>
Mitigation: Keep dashboards on localhost by default and add authentication before exposing any dashboard to a network. <br>


## Reference(s): <br>
- [ClawHub Dashboard Skill](https://clawhub.ai/ivangdavila/dashboard) <br>
- [Data source patterns](sources.md) <br>
- [Dashboard design rules](design.md) <br>
- [Dashboard widgets](widgets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated static HTML, JSON configuration, and bash fetch scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dashboards are stored under ~/dashboard/ and are intended for local hosting by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
