## Description:

开箱测评种草广告视频，用AI-HIVE完成原创多模型图像与视频制作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

品牌市场、电商商家、广告公司、门店和内容营销团队使用此 skill 为开箱测评种草广告视频生成原创计划、素材权利清单、模型路由、小样、广告脚本、成片任务记录和验收清单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send account credentials to any MCP URL supplied through AI_HIVE_MCP_URL.

Mitigation: Use the fixed AI-HIVE endpoint or OAuth client flow, keep API keys in a secret store, and set AI_HIVE_MCP_URL only when the destination is fully trusted.

Risk: Paid generation, bulk actions, sending, or publication can create cost or external distribution impact.

Mitigation: Confirm the selected model, budget, expected calls, and publication target before any paid, bulk, sending, or public release action.

Risk: Advertising outputs may contain unsupported claims or use media without adequate rights.

Mitigation: Maintain a product fact card and material rights list, use references only for mechanisms such as composition or pacing, and complete a compliance check before publication.

## Reference(s):

- [AI-HIVE 工作台](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [开箱测评种草广告视频：原创实施卡](references/original-workflow.md)
- [OAuth MCP 配置示例](references/mcp-config.example.json)
- [API Key MCP 配置示例](references/mcp-config-api-key.example.json)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-090-77ba653)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON work orders, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid generation, bulk actions, sending, and public publication require separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
