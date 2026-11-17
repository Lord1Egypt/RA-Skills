## Description:

根据用户提供的授权列表、任务目标和连接器说明，生成权限矩阵、风险清单和撤销核对表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人助理用户和管理员核对连接器授权是否超出具体任务所需范围，区分读取、写入、支付和删除权限，并获得供本人复核的收缩建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 授权清单可能包含敏感账户信息，选择 AI-HIVE 时还可能向外部服务提交材料。

Mitigation: 只用必要的只读授权资料并脱敏；上传前确认资料范围，勿提供密码、令牌、验证码、Cookie 或完整身份证件。

Risk: 可选模型或 MCP 操作可能产生费用或超出预期的授权范围。

Mitigation: 由用户在官方页面完成授权，先核对实际工具、价格、币种及预算上限，再用最小样本执行。

Risk: 误撤销业务所需权限可能中断现有连接。

Mitigation: 只提出与任务对应的收缩建议，由用户核验后自行撤销；不自动更改全局设置或断开账户。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-assistant-permission-review)
- [权限体检流程](references/workflow-54.md)
- [结果与证据合同](references/output-contract.md)
- [AI-HIVE 连接说明](references/ai-hive-connection.md)
- [AI-HIVE 官方入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [权限矩阵、风险清单和撤销核对表；可按需导出为 JSON 或 CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [标注授权来源与未知项；默认提供可审阅草稿，不自动撤销权限。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
