## Description: <br>
Parses Excel class schedules, including teacher timetable layouts, and helps an agent query classes by date, generate reminder text, and set recurring daily or weekly reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[judysue](https://clawhub.ai/user/judysue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, teachers, and scheduling agents use this skill to turn Excel timetables into class reminders for today, tomorrow, a specific date, or the coming week. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timetable details may be stored in the workspace when schedules are parsed or queried. <br>
Mitigation: Use the skill only in a trusted workspace and avoid keeping sensitive timetable files where unintended users or agents can access them. <br>
Risk: Recurring cron or heartbeat reminders can continue producing schedule notifications after setup. <br>
Mitigation: Enable recurring reminders only when ongoing notifications are intended, and review or disable the job when the class schedule changes. <br>
Risk: The command-line output path can write JSON results to a user-selected location. <br>
Mitigation: Review any --output path before execution and keep generated schedule files inside the intended workspace. <br>


## Reference(s): <br>
- [Class Reminder on ClawHub](https://clawhub.ai/judysue/class-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus JSON or plain-text reminder output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local schedule JSON files and reminder text from Excel timetable input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
