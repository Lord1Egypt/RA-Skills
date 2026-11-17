## Description:

将任务要求、实际工具回执、输出文件和人工标准整理成个人 Agent 的验收报告、证据表及返工清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和团队可用它核对 Agent 任务交付与真实证据，识别待核事项，并生成验收报告、证据表及返工清单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 仅凭 Agent 声明或离线结构检查误判交付已通过验收。

Mitigation: 核对真实产物及工具回执；缺少关键证据时保持待核，不标记为已验收。

Risk: 使用可选 AI-HIVE 服务时泄露私密材料或产生未预期费用。

Mitigation: 先确认工具、上传范围、价格与预算上限；最小化及脱敏材料，不提交密码、令牌或验证码。

Risk: 误将计划或提交状态视为外部操作成功，或在超时后重复执行付款、写入等操作。

Mitigation: 外部动作需单独授权并核对真实回执；结果不明时查询原任务状态，不盲目重试。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-agent-delivery-audit)
- [执行与验收流程](references/workflow-41.md)
- [结果、证据与离线校验](references/output-contract.md)
- [AI-HIVE 登录与接入](references/ai-hive-connection.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, guidance]

**Output Format:** [验收报告、证据表和返工清单；可选 JSON 或 CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [记录来源和任务状态；缺少实际检查证据时标为待核，不宣称验收通过。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
