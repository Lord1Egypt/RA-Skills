## Description: <br>
Gets the current date, time, and timezone from the local system and returns a formatted response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changsheng0804](https://clawhub.ai/user/changsheng0804) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer current time, date, weekday, and timezone questions or to capture a timestamp for logs and scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Time and date answers can be inaccurate if the host system clock or timezone is misconfigured. <br>
Mitigation: Confirm the runtime environment clock and timezone before relying on output for logs, scheduling, or other time-sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changsheng0804/current-time) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and formatted time text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local date command; output reflects the host system clock and configured timezone.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
