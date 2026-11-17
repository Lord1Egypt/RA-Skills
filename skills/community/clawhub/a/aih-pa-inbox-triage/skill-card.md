## Description:

根据用户选定的邮箱范围和分类标准，生成邮件分类清单、漏信检查表与建议规则，并在必要时通过已授权工具辅助分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

需要整理个人收件箱的用户可用它梳理邮件、识别待回复或可能错过期限的消息，并先审阅建议标签及规则，再决定是否授权修改邮箱。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 邮箱导出内容可能包含敏感信息或登录凭证。

Mitigation: 仅处理选定的邮件范围，不在聊天中索取密码、令牌、Cookie 或验证码；上传前先核实范围并脱敏。

Risk: 分类错误可能遗漏重要邮件，改标签、发送或删除可能产生意外后果。

Mitigation: 先只读预览并将疑似重要邮件留待人工复核；改标签、发送、删除等操作分别取得明确授权。

Risk: 连接 AI-HIVE 或调用付费模型可能扩大资料访问范围并产生费用。

Mitigation: 先核实实际工具与授权范围，确认报价和费用上限后再用最小样本；缺少权限或预算时停止。

## Reference(s):

- [ClawHub 技能发布页](https://clawhub.ai/wubin1836/skills/aih-pa-inbox-triage)
- [邮箱分流执行与验收](references/workflow-52.md)
- [AI-HIVE 登录与连接说明](references/ai-hive-connection.md)
- [结果与证据格式](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [CSV 分类清单、漏信检查表及建议规则]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [分类理由和待人工复核项；外部动作须单独授权。]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
