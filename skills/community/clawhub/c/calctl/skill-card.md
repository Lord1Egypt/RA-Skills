## Description: <br>
Manage Apple Calendar events via icalBuddy + AppleScript CLI <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainbat](https://clawhub.ai/user/rainbat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users on macOS use this skill to have an agent list calendars, show events, search upcoming events, and create Apple Calendar entries through calctl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read calendars and create persistent Apple Calendar events. <br>
Mitigation: Confirm the exact title, date, time, notes, and calendar before creating events, and prefer an explicit --calendar value over the default. <br>
Risk: An untrusted calctl executable on PATH could perform unintended calendar actions. <br>
Mitigation: Confirm that the calctl executable on PATH is trusted before using the skill. <br>


## Reference(s): <br>
- [Calctl ClawHub page](https://clawhub.ai/rainbat/calctl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that read calendar data or create persistent Apple Calendar events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
