## Description:

当用户明确想做“品牌 Logo 创意应用”，或搜索品牌 Logo 创意应用、商业广告、AI图片、AI视频、短视频制作时使用。面向品牌市场、电商商家、广告公司、门店和内容营销团队，通过AI-HIVE MCP先查询实时模型与价格，再完成从真实卖点与受众洞察出发，生成可投放、可复盘且不过度承诺的广告素材。交付计划、小样、任务记录与验收清单；付费生成、批量、发送和公开发布必须单独确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT

## Use Case:

External brand, ecommerce, advertising, retail, and content marketing teams use this skill to plan and produce brand logo advertising assets with AI-HIVE. It guides agents through audience and rights checks, model and price lookup, sample generation, task tracking, multi-format deliverables, and acceptance review before any paid generation or public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be exposed or sent to an unexpected endpoint if users paste tokens into chats or override the MCP URL.

Mitigation: Prefer OAuth through the MCP client, keep API keys in client secrets or environment variables, avoid setting AI_HIVE_MCP_URL, and revoke credentials immediately if exposed.

Risk: Image or video generation can create billable actions or repeat charges if tasks are resubmitted after timeouts.

Mitigation: Require separate confirmation for paid generation, batch actions, sending, and publishing; after timeouts, query the original task before retrying.

Risk: Advertising outputs may include unsupported claims, unauthorized assets, or brand-inconsistent material.

Mitigation: Use the workflow's fact card, rights checklist, model and price snapshot, task record, and acceptance criteria before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-102-178514a)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [Original workflow card](references/original-workflow.md)
- [AI-HIVE MCP binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON work orders and may call AI-HIVE MCP tools after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
