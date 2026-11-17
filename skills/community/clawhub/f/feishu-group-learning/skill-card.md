## Description:

自动分析飞书群消息，提取学习点和进化建议，并支持多群监控、关键词提取和定时报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolvzhao-lab](https://clawhub.ai/user/coolvzhao-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to analyze authorized Feishu group chats, summarize recent message activity, extract learning signals, and generate periodic recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports embedded reusable Feishu credentials.

Mitigation: Rotate the app secret before use and supply credentials through a secure user-controlled mechanism.

Risk: The security evidence reports fixed private group IDs and ignored documented chat configuration.

Mitigation: Configure only explicitly authorized chats and verify the skill reads those configured chat IDs before execution.

Risk: The skill can retain raw message-derived summaries in local OpenClaw memory and log files.

Mitigation: Confirm local retention is acceptable, limit stored content, and monitor or clear generated memory and log files according to the deployment policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolvzhao-lab/skills/feishu-group-learning)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text report with Markdown log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write analysis output to local OpenClaw memory and log files when run.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
