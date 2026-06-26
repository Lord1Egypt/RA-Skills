## Description: <br>
Workspace wellness break reminder with configurable work intervals, cooldowns, idle resets, quiet hours, per-day caps, and on/off/snooze/status controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxj0276](https://clawhub.ai/user/lxj0276) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace users use this skill to add optional, non-medical break reminders to OpenClaw sessions during long work periods. It helps configure reminder timing, quiet hours, snooze behavior, daily caps, heartbeat checks, and status controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default-on reminders, timezone settings, quiet hours, or daily caps may not match a workspace's expectations. <br>
Mitigation: Review the configuration before installing and adjust `enabled`, `timezone`, `quiet_hours`, and `daily_max_reminders` to fit the workspace. <br>
Risk: Break reminders may become unwanted or disruptive during active work. <br>
Mitigation: Use `/break off`, `/break snooze <minutes>`, or `/break status` to disable, pause, or inspect reminder behavior. <br>
Risk: Reminder text could be mistaken for health advice if expanded beyond the documented scope. <br>
Mitigation: Keep reminder copy practical and non-medical, and do not provide diagnosis or treatment advice. <br>


## Reference(s): <br>
- [Focus Break Reminder on ClawHub](https://clawhub.ai/lxj0276/focus-break-reminder) <br>
- [config.example.json](references/config.example.json) <br>
- [Focus Break Reminder - Test Cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should keep reminder copy concise, optional, non-medical, and easy to disable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
