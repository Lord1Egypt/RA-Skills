## Description: <br>
Google Calendar integration for viewing, creating, and managing calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilalmohamed187-cpu](https://clawhub.ai/user/bilalmohamed187-cpu) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External users and agents use this skill to read Google Calendar schedules, find availability, create or modify events with Pro access, and generate morning briefs after local OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pro write and delete commands can change Google Calendar data without an enforced confirmation barrier. <br>
Mitigation: Before any create, update, quick-add, or delete action, require the agent to show the exact event title, time, calendar, and action, and proceed only after explicit user confirmation. <br>
Risk: The skill requires Google Calendar OAuth access and stores local OAuth credentials and tokens. <br>
Mitigation: Grant access only if comfortable with the requested calendar scopes, and keep ~/.config/gcal-pro/client_secret.json and token.json private. <br>
Risk: The setup flow may show an unverified Google OAuth app warning. <br>
Mitigation: Continue through that warning only when the user created and recognizes the OAuth project. <br>


## Reference(s): <br>
- [Google Cloud Project Setup Guide](docs/GOOGLE_CLOUD_SETUP.md) <br>
- [Google Calendar API Quick Reference](references/api-quickref.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bilalmohamed187-cpu/gcal-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown-formatted calendar summaries, confirmations, setup guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or change Google Calendar data through local Python scripts depending on OAuth scopes and tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
