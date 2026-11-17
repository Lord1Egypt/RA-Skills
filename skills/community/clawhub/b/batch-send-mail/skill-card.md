## Description:

批量发送个性化邮件技能。读取表格（CSV/Excel）中的邮箱列表和变量，替换邮件模板中的占位符后批量发送邮件。支持 HTML 格式、通用附件、SMTP 配置和干运行预览模式。当用户需要批量发送个性化邮件、邮件营销、通知邮件时触发，即使他们说"批量发邮件"、"群发邮件"、"批量发送邮件"也要使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyifeng6](https://clawhub.ai/user/wangyifeng6)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to generate previews and send personalized bulk email from CSV or Excel recipient tables, templates, SMTP settings, optional CC recipients, and shared attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send bulk email through a configured SMTP account, so incorrect recipient lists, templates, CC entries, or attachments can expose information or send unintended messages.

Mitigation: Run dry-run previews first, review recipient and CC lists, confirm template substitutions, and verify attachments before actual sending.

Risk: Reusable SMTP credentials may be stored in plaintext in config/config.ini, and passing credentials through command-line arguments can expose secrets in shell history or process listings.

Mitigation: Prefer an SMTP-specific app password, avoid --sender-password when possible, and remove or protect config/config.ini after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyifeng6/skills/batch-send-mail)
- [Example contacts CSV](examples/example_contacts.csv)
- [Example email template](examples/example_template.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plaintext dry-run or send reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local SMTP configuration and uses recipient tables, templates, and attachments supplied by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
