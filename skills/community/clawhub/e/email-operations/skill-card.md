## Description: <br>
Email Operations lets an agent read, search, retrieve, and send email through IMAP and SMTP, including inbox listings, message details, attachments, text email, HTML email, and bulk sends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiweiweilai](https://clawhub.ai/user/yiweiweilai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate a configured mailbox: list and search messages, inspect message bodies and attachments, save attachments, and send text, HTML, or attachment-bearing email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access the configured mailbox and send email from it. <br>
Mitigation: Install only when mailbox access and send authority are acceptable, and use an app-specific password. <br>
Risk: The skill can send local files as attachments or send message content read from local files. <br>
Mitigation: Review recipients, subject, body, body-file paths, and attachment paths before sending. <br>
Risk: The skill can save email attachments using sender-provided filenames. <br>
Mitigation: Save attachments only into a disposable folder until filenames are sanitized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiweiweilai/email-operations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime methods return Python dictionaries/lists and write attachment files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mailbox credentials in a local .env file and can read mailbox contents, send email, and read or write attachment files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
