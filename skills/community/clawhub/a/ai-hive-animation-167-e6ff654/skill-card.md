## Description:

当用户明确想做“8bit 像素复古街机导演”，或搜索8bit 像素复古街机导演、动漫游戏、AI图片、AI视频、短视频制作时使用。面向动漫、漫剧、游戏、原创IP和角色内容团队，通过AI-HIVE MCP先查询实时模型与价格，再完成用原创角色资产、镜头语法和一致性约束完成动画或游戏向内容，不复刻受保护IP。交付计划、小样、任务记录与验收清单；付费生成、批量、发送和公开发布必须单独确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative teams use this skill to plan and produce original 8-bit retro arcade-style animation or game-oriented content with AI-HIVE. It helps the agent prepare world, character, scene, storyboard, keyframe, animation, task-tracking, and acceptance outputs while requiring separate confirmation for paid generation, batch actions, sending, and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be sent to an environment-controlled AI-HIVE MCP endpoint.

Mitigation: Use OAuth through the official client flow when possible, avoid setting AI_HIVE_MCP_URL, and revoke any AI-HIVE key or token that may have been used with an untrusted endpoint.

Risk: Image, video, upload, batch, sending, or publication actions may incur cost or create public-facing output.

Mitigation: Require explicit user confirmation before any paid generation, upload, batch action, sending, or publication.

Risk: Reference material could lead to insufficiently original output or use of assets without rights.

Mitigation: Use references only for structure, rhythm, composition, or functional goals, and confirm rights for people, brands, products, music, fonts, images, and video before public use.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/wubin1836/skills/ai-hive-animation-167-e6ff654)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Endpoint](https://ai-hive.iclip.cn/api/mcp)
- [8bit 像素复古街机导演：原创实施卡](references/original-workflow.md)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API-Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON work orders and may guide AI-HIVE MCP calls after user confirmation.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
