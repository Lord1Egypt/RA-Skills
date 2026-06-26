## Description: <br>
Feishu Meeting Reminder helps an agent create Feishu calendar meetings, add attendee reminders, and list, search, update, or delete meeting events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramlee77](https://clawhub.ai/user/ramlee77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents that work with Feishu calendars use this skill to create meetings with reminders, check upcoming events, search meeting records, and manage calendar changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, edit, delete, and notify Feishu calendar meetings without clear confirmation requirements. <br>
Mitigation: Require explicit user confirmation before creating, editing, deleting, adding attendees, creating video meetings, or sending notifications. <br>
Risk: Meeting notifications may be sent unintentionally. <br>
Mitigation: Keep notifications disabled unless the user explicitly asks to notify attendees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramlee77/feishu-meeting-reminder) <br>
- [Publisher profile](https://clawhub.ai/user/ramlee77) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON, API calls] <br>
**Output Format:** [Markdown guidance with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Feishu calendar event actions for create, list, get, patch, delete, and search workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
