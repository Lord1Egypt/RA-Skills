## Description: <br>
Manage calendar events by creating, viewing, updating, or deleting events using natural language commands via the Claw Calendar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5twang](https://clawhub.ai/user/5twang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage personal or work calendars after the user configures a Claw Calendar server URL and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to create, update, or delete calendar data. <br>
Mitigation: Require the agent to show the exact calendar and event details and obtain user confirmation before changes, especially for updates, deletes, and calendar-level actions. <br>
Risk: The skill requires a sensitive API key for calendar access. <br>
Mitigation: Use a revocable API key, keep it in the configured environment variable, and install only when the configured Claw Calendar server is trusted. <br>


## Reference(s): <br>
- [Claw Calendar API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/5twang/claw-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with API request details and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CALENDAR_API_BASE_URL and CALENDAR_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
