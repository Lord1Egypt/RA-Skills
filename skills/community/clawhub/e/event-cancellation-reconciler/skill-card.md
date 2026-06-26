## Description: <br>
Standard Operating Procedure (SOP) to autonomously detect cancelled events and sync the calendar state using atomic nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and calendar-management agents use this skill to reconcile Google Calendar entries after receiving cancellation or reschedule notices by extracting event details, searching the calendar, and marking or removing the affected event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete calendar events based on email-derived information without a clear user confirmation step. <br>
Mitigation: Add or enforce a manual preview and confirmation step before calendar writes. <br>
Risk: A weak event match could reconcile the wrong calendar entry. <br>
Mitigation: Require strong matching by title, organizer, date, and time before marking or deleting an event. <br>
Risk: Deleting events can remove useful audit context. <br>
Mitigation: Prefer marking events cancelled over deleting them when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/event-cancellation-reconciler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown instructions with inline shell commands and a final confirmation message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog command-line tool and calendar write authority.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
