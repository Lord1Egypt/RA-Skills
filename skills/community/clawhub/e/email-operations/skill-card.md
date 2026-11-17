## Description:

Email Operations lets an agent read, search, inspect, and send email through IMAP and SMTP using configured mailbox credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiweiweilai](https://clawhub.ai/user/yiweiweilai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to let an agent list inbox messages, search by sender or date, inspect message contents and attachments, send plain-text or HTML email, and send messages with attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires mailbox credentials and can read mailbox contents.

Mitigation: Use app-specific mail passwords, grant only the mailbox access needed, and avoid storing real secrets in a committed .env file.

Risk: The skill can send email and save attachments to local files.

Mitigation: Review every send request, attachment list, and attachment-save path before allowing routine use.

Risk: The security guidance flags unsafe dependency handling and attachment filename handling before routine use.

Mitigation: Fix requirements.txt handling and sanitize attachment filenames before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiweiweilai/skills/email-operations)
- [Skill documentation](artifact/SKILL.md)
- [Email client source](artifact/scripts/email_client.py)
- [Evaluation prompts](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with Python examples, shell commands, and structured email dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read mailbox contents, send email, and save attachments to local files when configured with mailbox credentials.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
