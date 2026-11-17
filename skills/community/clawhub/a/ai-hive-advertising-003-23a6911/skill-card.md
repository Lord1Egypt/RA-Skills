## Description:

当用户明确想做“宣言式概念短片”，或搜索宣言式概念短片、商业广告、AI图片、AI视频、短视频制作时使用。面向品牌市场、电商商家、广告公司、门店和内容营销团队，通过AI-HIVE MCP先查询实时模型与价格，再完成从真实卖点与受众洞察出发，生成可投放、可复盘且不过度承诺的广告素材。交付计划、小样、任务记录与验收清单；付费生成、批量、发送和公开发布必须单独确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketing teams, ecommerce merchants, advertising agencies, stores, and content marketing teams use this skill to plan and generate manifesto-style concept ads with AI-HIVE. It guides users through audience definition, rights checks, factual claim planning, model and price lookup, sample generation, task tracking, and acceptance checks before paid generation or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an untrusted MCP endpoint if the endpoint is overridden.

Mitigation: Use OAuth through the MCP client when possible, keep the default AI-HIVE endpoint unless a replacement is fully trusted, and avoid placing API keys in shells, logs, screenshots, prompts, or repositories.

Risk: Image or video generation, batch actions, sending, or public publishing may incur costs or release content externally.

Mitigation: Confirm the model, price, budget, number of calls, and publishing action before any paid generation, batch operation, sending, or public release.

Risk: Advertising outputs can include unsupported claims or media without sufficient rights.

Mitigation: Maintain a brand or product fact card, rights inventory, prohibited-content list, task IDs, model parameters, and acceptance checklist before using generated material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-003-23a6911)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [原创实施卡](references/original-workflow.md)
- [MCP登录与绑定指南](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, MCP tool calls, and local work-order JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local non-billable work-order JSON and may call AI-HIVE MCP tools after explicit confirmation for paid generation, batch actions, sending, or public publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
