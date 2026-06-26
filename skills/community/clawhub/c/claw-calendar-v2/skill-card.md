## Description: <br>
Claw Calendar Skill helps agents manage calendars and events through the Claw Calendar REST API using user-provided credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5twang](https://clawhub.ai/user/5twang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to list calendars, create calendars with subscription links, list events, and create calendar events with optional reminders in Claw Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Claw Calendar API key and can access connected calendar data. <br>
Mitigation: Store the API key only in environment variables, keep it out of repositories and logs, and rotate it periodically. <br>
Risk: A misconfigured API URL could send credentials or calendar data to an unintended endpoint. <br>
Mitigation: Verify CLAW_CALENDAR_API_URL before use and prefer the default Claw Calendar service URL unless a trusted alternate endpoint is required. <br>
Risk: Commands can create calendars, create events, set reminders, or print subscription links. <br>
Mitigation: Review command arguments and generated subscription links before sharing or relying on created calendar content. <br>


## Reference(s): <br>
- [Claw Calendar Skill on ClawHub](https://clawhub.ai/5twang/claw-calendar-v2) <br>
- [Publisher profile](https://clawhub.ai/user/5twang) <br>
- [Claw Calendar](https://claw-calendar.com) <br>
- [Claw Calendar API base URL](https://claw-calendar.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAW_CALENDAR_API_KEY and optional CLAW_CALENDAR_API_URL environment variables; scripts call the Claw Calendar REST API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
