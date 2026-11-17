## Description:

This skill helps brand, ecommerce, advertising, retail, and content marketing teams use AI-HIVE MCP to plan and produce theme-transformation advertising shorts with model and price checks, human confirmation gates, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External commercial users use this skill to create AI-HIVE advertising shorts from brand or product facts, authorized inputs, budget limits, and channel requirements. The skill produces plans, sample concepts, task records, creative assets, and review checklists while requiring explicit confirmation before paid generation, batch operations, sending, or public publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send API credentials to an arbitrary MCP endpoint when AI_HIVE_MCP_URL is overridden.

Mitigation: Use the default AI-HIVE endpoint unless the alternative endpoint is fully trusted, and revoke any key used with an untrusted endpoint.

Risk: Image and video generation tools may create paid tasks or public-facing advertising outputs.

Mitigation: Require explicit user confirmation before paid generation, uploads, batch actions, sending, or public publishing.

Risk: Advertising outputs can include unsupported product claims, unauthorized media, or copied reference work.

Mitigation: Use the fact card, rights checklist, and acceptance checklist to confirm claims, asset rights, originality, and publish readiness before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-012-986329b)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Endpoint](https://ai-hive.iclip.cn/api/mcp)
- [主题变身特效短片：原创实施卡](references/original-workflow.md)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON work orders and may call AI-HIVE MCP tools only after required credentials and confirmations are provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
