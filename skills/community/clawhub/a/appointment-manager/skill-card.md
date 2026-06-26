## Description: <br>
Books, tracks, and reminds users of appointments through online booking or phone-call scripts, managing the full appointment lifecycle and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to book, log, reschedule, cancel, and receive reminders for personal appointments. It supports online booking flows when browser booking is available and prepares phone-call scripts when providers require a call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real appointments, calendars, reminders, cancellations, and reschedules. <br>
Mitigation: Require explicit user confirmation before each booking, cancellation, reschedule, calendar change, or reminder-channel change. <br>
Risk: Appointment records may include sensitive personal or medical details such as visit reasons, dates of birth, provider history, or follow-up notes. <br>
Mitigation: Store only details needed for the appointment workflow, avoid unnecessary medical details, and review local appointment and provider files periodically. <br>
Risk: Reminder delivery through configured channels may expose appointment details to the wrong destination if preferences are stale or misconfigured. <br>
Mitigation: Confirm the delivery channel during setup and before sending sensitive reminders, and keep reminder text concise when privacy is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rednix/appointment-manager) <br>
- [Skill homepage](https://clawhub.com/skills/appointment-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown messages, local Markdown records, reminder payloads, and booking guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update appointment, provider, configuration, reminder, and calendar records when the user authorizes those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
