## Description: <br>
Monitor and summarize finance websites for fund-investing support. Use when user asks to fetch finance site text, track changes, or schedule periodic monitoring/briefings from a list of URLs (no login required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warriorfan](https://clawhub.ai/user/warriorfan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and finance-focused agents use this skill to fetch public no-login finance sources, summarize market and fund-related updates, compare current content with prior snapshots, and schedule periodic briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule recurring briefings with cron. <br>
Mitigation: Confirm the monitoring cadence and where the cron entry is created so the schedule can be disabled later. <br>
Risk: The skill can save rolling local snapshots of fetched finance-site text. <br>
Mitigation: Confirm where the state file is stored and delete saved snapshots when monitoring is no longer needed. <br>
Risk: Monitoring unintended or login-protected sources may create privacy, access, or compliance concerns. <br>
Mitigation: Use only confirmed public no-login URLs from the requested or default source list. <br>


## Reference(s): <br>
- [Finance Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings and status messages with optional shell commands for scheduling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a small local rolling snapshot for change monitoring and may propose cron scheduling when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
