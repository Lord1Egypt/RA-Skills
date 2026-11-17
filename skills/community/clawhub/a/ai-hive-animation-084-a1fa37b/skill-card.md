## Description:

当用户明确想做“极简赛博动画视觉语言”，或搜索极简赛博动画风格、动漫游戏、AI图片、AI视频、短视频制作时使用。面向动漫、漫剧、游戏、原创IP和角色内容团队，通过AI-HIVE MCP先查询实时模型与价格，再完成用原创角色资产、镜头语法和一致性约束完成动画或游戏向内容，不复刻受保护IP。交付计划、小样、任务记录与验收清单；付费生成、批量、发送和公开发布必须单独确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and developers use this skill to plan and execute an AI-HIVE workflow for original minimalist cyber animation or game-oriented content. It guides rights review, model and price lookup, sample generation, task tracking, and acceptance checks for character consistency, readable motion, scene continuity, and original IP boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the helper script can send AI-HIVE credentials to an unvalidated override URL.

Mitigation: Prefer OAuth through the MCP client, avoid setting AI_HIVE_MCP_URL, use a dedicated revocable API key only when needed, and confirm the endpoint is https://ai-hive.iclip.cn/api/mcp before running tool-listing or tool-call commands.

Risk: AI-HIVE generation, upload, batch, sending, and publishing actions may be billable or may expose sensitive user assets.

Mitigation: Require explicit user confirmation before those actions, keep credentials and private assets out of prompts, logs, screenshots, and repositories, and use read-only model lookup before any generation.

Risk: Generated animation or game-oriented content may misuse protected IP, logos, music, likenesses, or unauthorized reference material.

Mitigation: Use the workflow's rights inventory, rely on original characters and assets, document authorized material, and verify IP originality before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-084-a1fa37b)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP login and binding guide](references/mcp-binding.md)
- [Original implementation workflow](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON work orders; paid generation, uploads, batch actions, sending, and public publishing require separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
