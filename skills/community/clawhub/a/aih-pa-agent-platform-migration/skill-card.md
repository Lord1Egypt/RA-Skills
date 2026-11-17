## Description:

帮助迁移个人 Agent 的用户核对可导出的任务与偏好，并形成能力差异表、迁移步骤及验收清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户及其代理可用此技能梳理现有助理的任务、偏好与目标环境，区分可迁移能力和缺口，并以小样验证迁移结果；需要模型时可选择 AI-HIVE，但外部执行取决于实际工具与授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 迁移材料可能含敏感资料，外部上传可能超出用户预期。

Mitigation: 先确认上传范围并最小化、脱敏材料；不要收集密码、令牌、验证码、Cookie 或完整证件。

Risk: 可选模型调用或外部动作可能产生费用或改变用户数据。

Mitigation: 调用前确认实时价格、币种、预算和权限；付费、发送、删除、公开发布及业务系统修改分别取得明确授权。

Risk: 工具缺失或任务超时可能导致错误宣称迁移或外部操作已完成。

Mitigation: 保留缺项与原任务 ID，核对真实回执和产物后才报告完成；写入和付费操作不得盲目重试。

## Reference(s):

- [ClawHub 技能发布页](https://clawhub.ai/wubin1836/skills/aih-pa-agent-platform-migration)
- [迁移流程与验收](references/workflow-44.md)
- [结果与证据合同](references/output-contract.md)
- [AI-HIVE 登录与接入说明](references/ai-hive-connection.md)
- [AI-HIVE 网页入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [可审阅的能力差异表、迁移步骤和验收清单；按需提供 Markdown、CSV 或 JSON 文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [领域字段记录来源和未知状态；可用离线检查器校验结果结构与文件哈希，不代替实际验收。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
