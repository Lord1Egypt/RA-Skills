## Description:

一键读取 20+ 平台聊天，生成智能纪要（摘要、决策、行动项、风险、多维分析、AI 建议）。Auto-read 20+ platforms, generate smart minutes with summaries, decisions, actions, risks, multi-dimensional analysis, and AI suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaomo-1225](https://clawhub.ai/user/yaomo-1225)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and individual users use ChatMerge to summarize multi-channel chat activity into structured minutes, decisions, action items, risks, follow-ups, and role-specific briefs. It can work from configured chat channels, imported chat files, or pasted conversation text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests chat access and broad automation authority across local tools and chat sessions.

Mitigation: Limit access to specific channels and workspaces, avoid broad API tokens, and require approvals for actions beyond summarization.

Risk: Monitoring, scheduled delivery, task creation, and meeting recording or transcription can expose private conversations or send information to unintended destinations.

Mitigation: Disable these features by default or require explicit user approval, destination allowlists, and clear consent before capture or delivery.

Risk: Bash execution, file writes, session sends, and outbound integrations can change local state or external systems.

Mitigation: Use host-level restrictions, scoped credentials, and review checkpoints before writes, sends, task creation, or outbound delivery.

## Reference(s):

- [ChatMerge ClawHub listing](https://clawhub.ai/yaomo-1225/skills/chatmerge)
- [Input Contract](references/input-contract.md)
- [Config Schema](references/config-schema.md)
- [Output Examples](references/output-examples.md)
- [OpenClaw documentation](https://docs.openclaw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown summaries with optional JSON or YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decisions, action-item tables, risk sections, follow-up questions, analytics, and role-specific summary levels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
