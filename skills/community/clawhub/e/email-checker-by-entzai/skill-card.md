## Description: <br>
Automated email assistant for Apple Mail that scores unread messages, drafts AI replies, sends scheduled reports, and supports reply sending through Mail.app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[entzclaw](https://clawhub.ai/user/entzclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and macOS automation users use this skill to monitor a Mail.app inbox, prioritize unread messages, receive digest reports, and prepare or send replies after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mail automation and scheduled execution can read messages, send reports or replies, and mark messages as read. <br>
Mitigation: Install on a dedicated bot mailbox or VM, grant Mail automation only where intended, and review the generated crontab before enabling scheduled runs. <br>
Risk: Email content and thread context may be sent to a configured LLM provider. <br>
Mitigation: Use a local LLM or set the provider to none for sensitive mail, and verify provider settings before running checks. <br>
Risk: The security guidance identifies unsafe or incomplete AppleScript handling and plaintext API-key storage. <br>
Mitigation: Inspect or supply the missing get_unread_emails.scpt, verify the report recipient, and avoid important personal or business inboxes until those issues are fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/entzclaw/email-checker-by-entzai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/entzclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces email priority summaries, draft reply text, setup guidance, and Mail.app automation commands.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
