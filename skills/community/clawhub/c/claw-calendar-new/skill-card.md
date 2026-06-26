## Description: <br>
Create, view, update, and delete calendar events using the Claw Calendar API with natural language commands for scheduling and managing personal calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5twang](https://clawhub.ai/user/5twang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage personal calendar data through a configured Claw Calendar server, including creating, listing, updating, and deleting calendars and events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured API key can allow the agent to read or change calendar data. <br>
Mitigation: Use a trusted HTTPS Claw Calendar server and a revocable API key with the least access available. <br>
Risk: Natural language scheduling requests can be parsed into the wrong calendar, date, time, or event. <br>
Mitigation: Confirm the target calendar, event title, date, and time before creating, updating, or deleting events. <br>
Risk: Updates or deletes can remove or alter useful calendar records. <br>
Mitigation: Ask for explicit confirmation before destructive changes and review the API response after the operation. <br>


## Reference(s): <br>
- [Claw Calendar API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/5twang/claw-calendar-new) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CALENDAR_API_BASE_URL and CALENDAR_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
