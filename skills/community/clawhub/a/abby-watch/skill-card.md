## Description: <br>
Simple time display for Abby. Use when you need to know the current time or count down to a specific time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earnabitmore365](https://clawhub.ai/user/earnabitmore365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Abby Watch to display the current local time in simple or verbose form and to count down to a specified 24-hour HH:MM time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verbose output labels the time as Australia/Sydney while the script uses the machine's local time. <br>
Mitigation: Verify the host timezone or update timezone handling before relying on verbose timezone labels. <br>
Risk: Countdown input is limited to 24-hour HH:MM values and past target times roll forward. <br>
Mitigation: Validate the requested target time and review countdown output for the intended date. <br>


## Reference(s): <br>
- [Time Formats Reference](references/time-formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/earnabitmore365/abby-watch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text time strings and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local system time; countdown accepts HH:MM 24-hour input.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
