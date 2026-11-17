## Description:

将获准使用的跨渠道消息导出整理为统一任务收件箱、渠道映射和疑似重复清单，并保留每项任务的来源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

供需要整理微信、短信、Telegram 或 WhatsApp 待办的用户，将获准使用的渠道导出、身份映射和去重规则整理成可审阅的任务文件；模型辅助和外部操作取决于实际工具与授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private messages or tasks may be exposed across users or channels.

Mitigation: Use only authorized exports, separate users and conversations, and share summaries only within the approved disclosure scope.

Risk: Sensitive data or credentials may be exposed when uploading materials or connecting tools.

Mitigation: Redact and minimize materials before approved uploads; never request passwords, tokens, verification codes, cookies, or complete identity documents.

Risk: Paid requests or external changes may occur without informed approval.

Mitigation: Confirm price, currency, budget and scope before paid use, and require explicit approval before sending, deleting, or changing external systems.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-channel-task-inbox)
- [执行与验收流程](artifact/references/workflow-21.md)
- [结果与校验要求](artifact/references/output-contract.md)
- [AI-HIVE 连接说明](artifact/references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [CSV and Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [统一任务收件箱、渠道映射及疑似重复清单；各任务保留来源和允许披露的范围。]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
