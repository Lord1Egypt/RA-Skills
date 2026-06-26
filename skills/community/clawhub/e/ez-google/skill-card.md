## Description: <br>
Use when asked to send email, check inbox, read emails, check calendar, schedule meetings, create events, search Google Drive, create Google Docs, read or write spreadsheets, find contacts, or any task involving Gmail, Google Calendar, Drive, Docs, Sheets, Slides, or Contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to help users operate Google Workspace services from CLI commands, including Gmail, Calendar, Drive, Docs, Sheets, Slides, Contacts, and Workspace Chat. It is intended for users who want agent-mediated Google Workspace actions without manually configuring API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad, long-lived Google Workspace access through a third-party hosted OAuth flow. <br>
Mitigation: Use a dedicated or low-risk Google account, review Google's consent screen carefully, and revoke the OAuth grant when finished. <br>
Risk: Gmail bulk operations can label or trash many messages, and the bulk-trash command supports a flag that skips confirmation. <br>
Mitigation: Review the exact Gmail query before running bulk operations and avoid the confirmation bypass unless the intended message set has been explicitly approved. <br>
Risk: The scripts can create, modify, send, download, or delete Workspace content after authentication. <br>
Mitigation: Run only narrowly scoped commands, inspect command arguments before execution, and prefer accounts with limited data exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/ez-google) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/araa47) <br>
- [Hosted OAuth service used by the artifact](https://ezagentauth.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read, create, modify, send, download, or delete Google Workspace content depending on the selected script and OAuth grant.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
