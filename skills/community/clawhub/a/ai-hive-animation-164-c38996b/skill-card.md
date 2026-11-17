## Description:

Helps animation, comics, game, original IP, and character-content teams plan and produce an AI-HIVE-powered "million protagonists entrance animation" workflow with original character assets, model and price checks, storyboard planning, sample generation, task tracking, and acceptance checks while requiring separate confirmation for paid generation, batch actions, sending, or public publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative teams and developers use this skill to turn a short animation or game-content brief into a rights-aware production plan, storyboard, AI-HIVE model route, small sample, task record, generated assets, and acceptance checklist. It is especially aimed at workflows that need character consistency, readable action, scene continuity, and original-IP controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be sent to an unintended MCP endpoint if AI_HIVE_MCP_URL is changed.

Mitigation: Use OAuth or API keys only with the official AI-HIVE endpoint, avoid setting AI_HIVE_MCP_URL unless the destination is fully trusted, and revoke any key exposed to the wrong host.

Risk: The MCP/tool scope includes generation, upload, batch, send, and publishing actions that may incur cost or expose content.

Mitigation: Require explicit confirmation before any paid generation, upload, batch, send, or public publishing action.

Risk: Generated character or media outputs can raise rights and originality concerns when source material or references are not authorized.

Mitigation: Maintain a material-rights list, use references only for structure or mechanics, and verify that people, brands, products, music, fonts, images, and video have necessary rights before public use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-164-c38996b)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [MCP 登录与绑定指南](references/mcp-binding.md)
- [百万主角登场动效：原创实施卡](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON work orders and AI-HIVE task records; paid generation, upload, batch, send, and publishing actions require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
