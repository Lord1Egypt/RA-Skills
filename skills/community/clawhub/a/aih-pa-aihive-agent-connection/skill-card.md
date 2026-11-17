## Description:

帮助个人助理用户核对 AI-HIVE 接入条件、可用能力和费用边界，并整理脱敏调用回执。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和智能体开发者使用本技能核对客户端与 AI-HIVE 的网页或远程 MCP 接入条件，并制作接入核对表、能力矩阵和脱敏调用回执。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 聊天中泄露账户凭证或敏感资料。

Mitigation: 由用户在官方页面授权；不在聊天中索要密码或 Token，上传前确认资料范围并脱敏。

Risk: 未经确认的上传或付费调用造成数据外传或超支。

Mitigation: 执行前确认上传范围、当前报价、币种和费用上限，先用最小样本验证。

Risk: 将本地校验通过误认为 AI-HIVE 操作已成功。

Mitigation: 本地检查仅验证结构和文件哈希；用真实工具回执和输出核对外部结果。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-aihive-agent-connection)
- [AI-HIVE web access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [AI-HIVE protected resource metadata](https://ai-hive.iclip.cn/.well-known/oauth-protected-resource/api/mcp)
- [AI-HIVE authorization server metadata](https://ai-hive.iclip.cn/.well-known/oauth-authorization-server)
- [Connection and authorization guidance](references/ai-hive-connection.md)
- [Output and verification contract](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [接入核对表、能力矩阵和脱敏调用回执；可按需导出 JSON 或 CSV。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [实际工具调用和结果须核对；缺少工具时仅交付可审阅草稿。]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
