## Description: <br>
Natural language reminders that create actual Apple Reminders.app entries (macOS-native) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill on macOS to create, list, complete, delete, and reschedule Apple Reminders using natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit, complete, and delete real reminders that may sync across Apple devices. <br>
Mitigation: Review the matched reminder ID and title before running edit, complete, or delete actions. <br>
Risk: Delete actions may be permanent. <br>
Mitigation: Confirm deletion intent before execution and avoid deleting reminders unless the user clearly requested it. <br>
Risk: The skill depends on remindctl for access to Apple Reminders. <br>
Mitigation: Verify that remindctl is installed from a trusted source before allowing the skill to manage reminders. <br>


## Reference(s): <br>
- [Apple Reminder ClawHub release](https://clawhub.ai/plgonzalezrx8/apple-remind-me) <br>
- [Publisher profile](https://clawhub.ai/user/plgonzalezrx8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses macOS Apple Reminders through remindctl and returns reminder IDs, titles, due dates, and action status messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
