## Description: <br>
Send and receive emails with the Resend API, including direct sends, inbound cron notifications, threaded reply drafting, and attachment downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivelin](https://clawhub.ai/user/ivelin) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agents use this skill to send email through Resend, monitor inbound messages, draft threaded replies, configure recurring notifications, and download received attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private email and requires Resend API access. <br>
Mitigation: Install only when email access is intended, use a least-privileged Resend key, and keep email data available only to trusted agents. <br>
Risk: Recurring inbound checks can send email summaries to an incorrect or stale chat destination. <br>
Mitigation: Before enabling cron, replace hardcoded Telegram examples, verify the configured chat and topic, and confirm how to remove the cron job. <br>
Risk: Downloaded attachments may have untrusted filenames or contents. <br>
Mitigation: Download attachments only to a controlled folder and treat both filenames and file contents as untrusted. <br>
Risk: Automatic confirmation can send outbound email without an interactive review. <br>
Mitigation: Avoid the --yes path except in trusted automation and preview outbound messages before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivelin/email-resend) <br>
- [Resend](https://resend.com) <br>
- [Resend API](https://api.resend.com) <br>
- [Custody chain design](docs/custody-chain.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, JSON script output, and email text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RESEND_API_KEY and optional sender and notification preferences; can create recurring cron notifications and local email state files.] <br>

## Skill Version(s): <br>
1.0.14 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
