## Description: <br>
Detects scheduling conflicts before booking meetings by checking attendee free/busy status, finding shared available time slots, and warning before event creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramlee77](https://clawhub.ai/user/ramlee77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to check Feishu calendar availability for named attendees, identify shared meeting windows, and avoid creating conflicting calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar availability queries can expose sensitive schedule information or include people outside the intended meeting scope. <br>
Mitigation: Use the skill only with appropriate workplace authorization and keep queries limited to named attendees and specific time windows. <br>
Risk: The skill can support event creation after conflict checks, which may affect attendee calendars if executed without review. <br>
Mitigation: Require explicit confirmation before creating any calendar event. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramlee77/feishu-calendar-conflict) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces availability checks, suggested free time windows, and conflict warnings before calendar event creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
