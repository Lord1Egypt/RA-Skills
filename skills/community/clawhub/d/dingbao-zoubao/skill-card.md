## Description:

每天定时生成综合、财经、科技、AI 和股市等主题的个性化中文早报，并在配置后推送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to generate recurring or manually triggered Chinese-language daily briefings across general news, finance, technology, AI, and stock-market topics. When a Feishu chat is configured, the skill can deliver the generated briefing to that chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated briefings may be sent to a configured Feishu chat that is broader than intended.

Mitigation: Confirm the Feishu chat ID before installation and remove feishu_chat_id when only local report generation is desired.

Risk: Broad trigger phrases in shared or automated contexts can generate and send reports unintentionally.

Mitigation: Use explicit trigger phrasing and review automation rules before enabling scheduled delivery.

Risk: Briefing content may summarize fast-changing news, finance, technology, AI, or stock-market topics inaccurately or incompletely.

Mitigation: Review important generated briefings and verify source articles before making decisions from them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/dingbao-zoubao)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Chinese-language briefing text, with optional Feishu rich-text message delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topic is inferred from the user request; configured Feishu chat delivery sends the generated report outside the local agent session.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
