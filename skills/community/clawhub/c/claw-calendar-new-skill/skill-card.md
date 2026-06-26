## Description: <br>
Calendar Skills intelligent calendar assistant: interacts with Claw Calendar (claw-calendar.com) through REST APIs to manage calendars and events, reading credentials from environment variables and supporting calendar creation, event creation, and schedule queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5twang](https://clawhub.ai/user/5twang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list calendars, create calendars, list events, and create events in Claw Calendar from an agent workflow. It is useful when calendar IDs, event details, reminders, or subscription links need to be managed through the Claw Calendar API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Claw Calendar API key to access calendar data. <br>
Mitigation: Keep the API key private, provide it only through CLAW_CALENDAR_API_KEY, and avoid storing it in repositories, prompts, or logs. <br>
Risk: Changing CLAW_CALENDAR_API_URL can send credentials and calendar data to a replacement endpoint. <br>
Mitigation: Leave CLAW_CALENDAR_API_URL unset unless the replacement endpoint is trusted. <br>
Risk: The skill can create calendars and events and return subscription links that may expose calendar information if shared. <br>
Mitigation: Review calendar IDs, event details, reminders, and subscription links before using or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/5twang/claw-calendar-new-skill) <br>
- [Claw Calendar service](https://claw-calendar.com) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_CALENDAR_API_KEY and optionally CLAW_CALENDAR_API_URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
