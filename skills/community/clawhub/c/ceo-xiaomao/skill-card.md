## Description:

CEO小茂聚合技能包。用于外贸 CEO/业务负责人场景：协调汇报、Google Maps 商务联系人收集、OneABC 模型调用、邮件发送、WhatsApp 消息发送、WhatsApp 会话助理，并支持一键初始化模板文件。适用于想安装后快速搭建一套可配置业务工作流的人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfan0828](https://clawhub.ai/user/xingfan0828)

### License/Terms of Use:

MIT-0

## Use Case:

External business owners, trade operators, and sales teams use this skill to coordinate foreign-trade workflows, source leads, prepare outreach, send email or WhatsApp messages, and initialize configurable workspace templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically monitor WhatsApp chats and retain customer or intent data.

Mitigation: Review carefully before installing, test with non-production accounts and recipients, confirm customer consent for monitoring and retention, and restrict workspace file permissions.

Risk: The skill can send messages and files automatically to customers or leads.

Mitigation: Review recipient lists, templates, and product assets before dispatch; keep pacing conservative; and disable or supervise auto-discovery, unconditional catalog sending, and unattended auto-reply loops until patched.

Risk: The skill can fetch and process media from external URLs.

Mitigation: Use only trusted HTTPS provider endpoints and patch or disable unvalidated media downloads before running the auto-reply loop unattended.

## Reference(s):

- [CEO小茂 Coordination Method](artifact/references/coordination-method.md)
- [ClawHub skill page](https://clawhub.ai/xingfan0828/skills/ceo-xiaomao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated JSON and CSV configuration files, and script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize workspace templates, write logs, and produce customer outreach or management summaries when configured and executed.]

## Skill Version(s):

1.8.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
