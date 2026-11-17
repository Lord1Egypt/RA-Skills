## Description:

AI 与科技行业实时追踪 Skill。监控技术趋势、应用落地、公司动态、人物观点四大模块，支持多语言多平台来源，每日定时发送结构化摘要，重大事件即时发现并推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[billxfan](https://clawhub.ai/user/billxfan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to monitor recent AI and technology news across Chinese and English sources, generate structured Chinese-language daily digests, and send urgent event updates to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends generated news summaries to Feishu using a recipient read from workspace memory.

Mitigation: Review workspace memory for private notes, identifiers, tokens, or unrelated data before installation, and prefer a dedicated recipient configuration.

Risk: The skill deletes the draft after sending, which can reduce auditability of what was delivered.

Mitigation: Decide before deployment whether automatic draft deletion fits audit requirements, or retain delivery logs through an approved process.

Risk: News tracking can include stale, duplicated, or misdated events if event time is not verified.

Mitigation: Use the skill's stated 48-hour and 12-hour event windows, require source links, and review important alerts before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billxfan/skills/ai-news-tracker)
- [Publisher profile](https://clawhub.ai/user/billxfan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest text with source links, Feishu message content, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily summaries use a 48-hour event window; urgent updates use a 12-hour event window and deduplicate repeated events.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
