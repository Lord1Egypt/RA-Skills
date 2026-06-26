## Description: <br>
Birthday Reminder helps users add, list, query, remove, and receive reminders for birthdays while calculating ages and upcoming birthday dates from local data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manantra](https://clawhub.ai/user/Manantra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to remember birthdays, ask when someone's birthday is, list upcoming birthdays, calculate ages, and generate reminder messages for birthdays stored on the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves names and birthdays locally, and that data remains on disk until removed. <br>
Mitigation: Use the skill only for birthday data you are comfortable keeping on this machine, and remove records when they are no longer needed. <br>
Risk: The documentation mentions birthdays.md, while the security evidence identifies /home/clawd/clawd/data/birthdays.json as the actual storage file. <br>
Mitigation: Treat /home/clawd/clawd/data/birthdays.json as the authoritative storage path when reviewing, backing up, or deleting birthday data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Manantra/birthday-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and formatted reminder text with optional Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and reads birthday records locally, then returns sorted birthday lists, next-birthday answers, age calculations, and 7-day, 1-day, or same-day reminder messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
