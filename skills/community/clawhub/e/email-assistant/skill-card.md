## Description: <br>
Email Assistant helps agents manage Gmail, 163, QQ, Outlook, and Hotmail accounts by fetching inbox summaries, identifying important messages by keyword, and extracting calendar events from email content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents managing multiple mailboxes use this skill to fetch and search email summaries, detect important messages, and convert schedule information from emails into calendar files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox access can expose sensitive email content, credentials, and local token files. <br>
Mitigation: Use revocable app passwords or least-privilege OAuth scopes, avoid command-line passwords, and keep credentials, tokens, and exported email files private. <br>
Risk: The Gmail client can modify mailbox state by marking messages. <br>
Mitigation: Review or disable message-modification behavior before use, and use read-only OAuth scopes unless mailbox changes are required. <br>
Risk: Cached OAuth tokens are stored locally using pickle. <br>
Mitigation: Replace pickle token storage with a protected credential store or another safer local credential format before production use. <br>


## Reference(s): <br>
- [Email configuration guide](references/email_config.md) <br>
- [Gmail API Python quickstart](https://developers.google.com/gmail/api/quickstart/python) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with shell command examples, Python scripts, JSON email analysis, and ICS calendar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided mailbox credentials or OAuth configuration; local outputs may include email content and calendar event data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
