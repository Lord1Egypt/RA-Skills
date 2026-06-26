## Description: <br>
Meeting prep - pull context on attendees, topics, and action items before every calendar event. Auto or on-demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business users use this skill to generate meeting prep briefs from calendar events, attendee context, recent communications, notes, and open tasks before scheduled meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting prep can expose sensitive calendar, inbox, CRM, task, and notes data. <br>
Mitigation: Before installing, decide exactly which data sources the skill may read and limit access to the calendars, inboxes, contact stores, task systems, and note stores needed for the workflow. <br>
Risk: Automatic prep briefs may deliver sensitive work context to the wrong place or at the wrong time. <br>
Mitigation: Keep auto-prep opt-in, use private delivery channels, and set a short email lookback window. <br>
Risk: Follow-up notes, tasks, or contact updates may be saved inaccurately if generated without review. <br>
Mitigation: Require confirmation before saving notes, creating tasks, or updating contacts. <br>


## Reference(s): <br>
- [DoctorClaw Meeting Prep on ClawHub](https://clawhub.ai/ceobotson-bot/doctorclaw-meeting-prep) <br>
- [DoctorClaw](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown meeting prep briefs with suggested talking points, attendee context, action items, and follow-up notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links or summaries from calendars, email, CRM/contact notes, task systems, and meeting-note storage when the user grants access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
