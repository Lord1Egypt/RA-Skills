## Description:

将用户选定的截图、语音或通知整理为可复核的待办清单、来源索引和日历导入内容，并标注待确认的时间信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和家庭可将自行选定的截图、语音和学校通知整理为可勾选的待办事项及待确认的日历内容；需要识别工具才能处理图像或语音。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 识别错误或相对日期可能导致错误的提醒。

Mitigation: 保留来源与置信度，对年份缺失、相对日期和低置信结果请求确认后再生成确定事件。

Risk: 连接外部服务时可能上传敏感材料或产生费用。

Mitigation: 仅使用用户选定的材料；上传或付费前核对工具、权限、报价、币种和预算，不索取密码或令牌。

Risk: 草稿或未完成的外部操作可能被误报为已完成。

Mitigation: 仅在获得真实产物并复核后报告完成；缺少工具或回执时列明待完成事项。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-capture-to-actions)
- [任务流程与验收](references/workflow-13.md)
- [结果与证据合同](references/output-contract.md)
- [AI-HIVE 登录与接入](references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Calendar import content]

**Output Format:** [可审阅的待办清单 JSON、来源索引和日历导入内容]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [包含来源引用、识别置信度和待确认标记；不确定的日期不生成确定的日历事件。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
