## Description: <br>
Queries and analyzes DingTalk attendance and clock-in records, summarizing exceptions such as late arrivals, early departures, absences, and attendance trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Golden-Pigeon](https://clawhub.ai/user/Golden-Pigeon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized HR, operations, or management users can use this skill to query DingTalk attendance data over natural-language date ranges and receive concise summaries of attendance anomalies, severity, and trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive employee attendance data through DingTalk credentials. <br>
Mitigation: Use only when authorized, configure a least-privileged DingTalk app, and protect the AppSecret and administrator phone configuration. <br>
Risk: Broad date ranges or organization scopes may retrieve more attendance data than needed. <br>
Mitigation: Limit queries to the required time period and organizational scope before running the attendance query. <br>
Risk: Generated SQLite cache and history files may persist sensitive attendance data locally. <br>
Mitigation: Store the cache in a secured location and delete or rotate it according to organizational data-retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Golden-Pigeon/dingtalk-attendance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run a local Python query script, call DingTalk APIs, and read or write a local SQLite cache when authorized credentials are configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
