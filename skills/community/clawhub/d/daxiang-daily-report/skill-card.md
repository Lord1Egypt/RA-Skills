## Description:

生成大象（即时通讯工具）每日沟通分析报告，自动汇总个人对话、群聊消息，按时间段分析沟通频率，识别活跃联系人，并生成结构化沟通摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kindhf](https://clawhub.ai/user/kindhf)

### License/Terms of Use:

MIT-0

## Use Case:

Employees who use Daxiang can generate a daily communication report from local or DX CLI-provided chat records. The report summarizes personal chats, group activity, time distribution, notable contacts, overall communication patterns, and potential todo items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive workplace conversations may be collected and stored in local JSON and Markdown report files.

Mitigation: Install only with authorization to process the involved Daxiang conversations, store generated files in access-controlled locations, and define retention rules before use.

Risk: Automatic DX fetching and scheduled execution can broaden collection beyond a manually reviewed export.

Mitigation: Prefer manually scoped exports unless automated collection is approved, and enable cron only after data access and retention controls are clear.

Risk: The artifact recommends installing DX CLI from an HTTP npm registry.

Mitigation: Use a trusted, pinned installation source and review the dependency path before installing or executing DX CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kindhf/skills/daxiang-daily-report)
- [Publisher profile](https://clawhub.ai/user/kindhf)
- [OpenClaw documentation](https://openclaw.com/docs)
- [Daxiang web application](https://x.sankuai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report file with console status text and optional configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are date-scoped and include data overview, time distribution, person and group summaries, overall insights, and todo items.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
