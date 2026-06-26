## Description: <br>
Automate email processing: smart triage, auto-categorization, draft replies, and inbox zero. Works with Gmail, Outlook, and IMAP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to triage Gmail, Outlook, or IMAP inboxes, categorize messages, draft replies, summarize inbox activity, and archive lower-priority email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox access credentials or tokens for Gmail, Outlook, or IMAP. <br>
Mitigation: Use least-privilege OAuth scopes or app passwords where available, store credentials outside shared workspaces, and rotate or revoke credentials after testing. <br>
Risk: Auto-archive defaults to enabled and can move newsletters, notifications, and receipts without additional confirmation. <br>
Mitigation: Set AUTO_ARCHIVE=false for initial runs, test against a noncritical inbox, and review categorized actions before enabling automatic archiving. <br>
Risk: The skill records processed email identifiers and run history in .email-automation/processed.json. <br>
Mitigation: Set EMAIL_AUTOMATION_DATA_DIR to a protected location and review retention or deletion practices for the local processing-history file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fly3094/email-automation) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Microsoft Azure Portal](https://portal.azure.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with setup commands, inbox summaries, categorized email lists, draft reply text, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local .email-automation/processed.json processing-history file.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
