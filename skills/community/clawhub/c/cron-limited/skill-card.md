## Description: <br>
Creates limited-repeat OpenClaw cron reminders that remove themselves after the requested number of runs, and supports lunar birthday reminders with optional yearly recurrence and advance notice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhiyongcn-coder](https://clawhub.ai/user/yuzhiyongcn-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to schedule reminders that repeat only a fixed number of times, or to configure lunar birthday reminders that can recur yearly with a chosen reminder time and advance notice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent scheduled messages and stores reminder data locally. <br>
Mitigation: Review the generated schedules and local reminder configuration before installing, use trusted recipients and channels only, and remove cron entries or stored reminders when they are no longer needed. <br>
Risk: The security evidence reports unsafe scripting that could execute crafted local input. <br>
Mitigation: Avoid untrusted reminder text, channel, recipient, lunar date, or timing values until inputs are safely serialized and the Python environment is explicitly trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw CLI, jq, and Python with lunarcalendar for lunar reminders.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
