## Description: <br>
Calendar Manager skill that converts Chinese natural-language event descriptions into importable .ics calendar files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Chinese event text such as meeting times, durations, titles, and dates into .ics files for Google Calendar, Apple Calendar, and Outlook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated calendar entries may reflect incorrect parsing of natural-language dates, times, titles, or durations. <br>
Mitigation: Review the printed event title, date, time, duration, and imported calendar entry before relying on it. <br>
Risk: The script writes an .ics file to the user's home directory. <br>
Mitigation: Run it in a trusted environment and inspect or remove generated files when they are no longer needed. <br>
Risk: Server security guidance limits installation to trusted ClawHub maintainer or Convex development environments. <br>
Mitigation: Follow the documented confirmation and opt-out controls when using powerful maintainer commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-calendar-manager) <br>
- [AISoBrand](https://aisobrand.com) <br>
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [ICS calendar file plus terminal status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a calendar_YYYYMMDD_title.ics file to the user's home directory.] <br>

## Skill Version(s): <br>
1.2.6 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
