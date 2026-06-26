## Description: <br>
Google Calendar integration for viewing, creating, and managing calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilalmohamed187-cpu](https://clawhub.ai/user/bilalmohamed187-cpu) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External users and agents use this skill to inspect Google Calendar schedules, search events, find free time, and, with Pro access, create, update, delete, or summarize events through natural-language calendar workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar write and delete operations can affect a user's live Google Calendar, and the security summary notes that confirmation relies too much on caller discipline. <br>
Mitigation: Use read-only mode unless write access is needed, and require an explicit preview plus confirmation before create, update, quick-add, or delete actions. <br>
Risk: The skill requires Google Calendar OAuth access and stores credentials under ~/.config/gcal-pro. <br>
Mitigation: Install only when comfortable granting Calendar access, protect the config directory, and avoid sharing or printing credential files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bilalmohamed187-cpu/gcal-pro-calendar) <br>
- [Google Cloud Project Setup Guide](docs/GOOGLE_CLOUD_SETUP.md) <br>
- [Google Calendar API Quick Reference](references/api-quickref.md) <br>
- [Google Calendar API](https://www.googleapis.com/calendar/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and calendar summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Google Calendar APIs through local Python scripts after OAuth setup and may require Pro access for write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
