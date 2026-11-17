## Description:

帮助办公用户续办未完成任务、整理工作文件并将资料转为可验收成果，按需通过已授权工具接入 AI-HIVE。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

办公用户可以将未完成任务续办、工作文件整理与资料转成果组合成可追踪的交付流程，核对实际文件、来源和验收状态。缺少必要工具或授权时，交付可审阅草稿及待办事项，而不声称完成外部操作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 机密资料或登录凭证可能被不当分享或上传。

Mitigation: 仅通过官方浏览器/OAuth 授权；不在聊天中提供密码、令牌、Cookie 或验证码，上传前确认范围并尽量脱敏。

Risk: 付费调用或文件改动可能超出用户预期。

Mitigation: 先预览变更、报价和费用上限，取得明确授权后从最小样本开始，文件改动优先保留原件并生成副本。

Risk: 发送、删除、公开发布或超时重试可能造成不可逆后果。

Mitigation: 逐项取得明确授权；结果不明时先核查原任务状态，不盲目重复执行。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-cowork-office-delivery)
- [Workflow and product scope](artifact/references/scope-and-sources.md)
- [AI-HIVE connection and authorization](artifact/references/ai-hive-connection.md)
- [Result and evidence requirements](artifact/references/output-contract.md)
- [Claude Cowork documentation](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- [Copilot Tasks documentation](https://support.microsoft.com/en-us/microsoft-copilot/using-copilot-tasks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [可审阅文本及任务相关文件，包括 CSV 和 JSON 记录]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [记录来源、实际产物和验收状态；未经核验的外部操作不得标为完成。]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
