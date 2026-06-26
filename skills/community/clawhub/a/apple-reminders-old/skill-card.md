## Description: <br>
Manage Apple Reminders via remindctl CLI, including listing, adding, editing, completing, and deleting reminders with list, date, JSON, and plain text support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents on macOS use this skill to manage Apple Reminders through the remindctl command line tool, including creating, listing, completing, and deleting reminders that sync with Apple's Reminders app. It also helps distinguish Apple Reminders tasks from agent-local alerts or scheduling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder or list deletion can remove user data, especially when commands use --force or list --delete. <br>
Mitigation: Confirm the exact reminder or list before allowing delete actions. <br>
Risk: The skill manages personal Apple Reminders data through remindctl after macOS Reminders permission is granted. <br>
Mitigation: Install and authorize it only on trusted macOS systems where agent access to Reminders is intended. <br>


## Reference(s): <br>
- [Apple Reminders.Old on ClawHub](https://clawhub.ai/huangfeng1995/apple-reminders-old) <br>
- [remindctl GitHub repository](https://github.com/steipete/remindctl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON or plain text remindctl output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires the remindctl binary and Apple Reminders permission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
