## Description:

将个人琐事委托拆分为可核验的任务，整理预约、购物、售后、订阅和出行的交付物与办结回执。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户可借助智能体拆分多阶段生活事务，制作待确认清单、比价或预约草稿，并依据实际凭证核对办理状态。实际对外操作取决于可用工具及单独授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 委托内容可能含账单、订单、行程及身份信息。

Mitigation: 仅分享任务必需的脱敏资料；不要在聊天中提交密码、令牌、验证码或完整身份证件。

Risk: 连接 AI-HIVE 可能涉及第三方授权、上传与付费。

Mitigation: 连接前核对官方域名、工具权限、上传范围、报价币种及预算，并先用小样本验证。

Risk: 未经确认的付款、退款、取消或对外发送可能造成不可逆影响。

Mitigation: 各项对外操作分别获得明确授权；状态不明时先核对实际回执，不盲目重试。

Risk: 草稿或本地检查通过可能被误认作已实际办结。

Mitigation: 核对真实服务回执与产物后才标记办结；工具不可用时明确列出未执行步骤。

## Reference(s):

- [ClawHub 技能发布页](https://clawhub.ai/wubin1836/skills/aih-pa-instinct-errand-receipts)
- [AI-HIVE 网页入口](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP 连接地址](https://ai-hive.iclip.cn/api/mcp)
- [产品身份与来源](artifact/references/scope-and-sources.md)
- [结果与证据合同](artifact/references/output-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Calendar files, Guidance]

**Output Format:** [任务清单、可审阅草稿和带证据引用的状态记录；按需导出 JSON、CSV 或 ICS 文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [仅在核对真实产物与回执后标记完成；缺少工具或授权时说明未执行事项。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
