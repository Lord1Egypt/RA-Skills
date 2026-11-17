## Description:

Guides anime, game, original IP, and character-content teams through an AI-HIVE workflow for original 1990s magical-girl-style image and video production, including planning, model and price checks, samples, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, animation teams, game teams, and original-IP content teams use this skill to plan and execute AI-HIVE image and video generation for original 1990s magical-girl-style content. The workflow emphasizes rights checks, model and price lookup, budget confirmation, task tracking, and review of character consistency, motion readability, scene continuity, and IP originality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be exposed or sent to an unintended endpoint if API keys are stored insecurely or AI_HIVE_MCP_URL is changed to an untrusted URL.

Mitigation: Prefer OAuth through the MCP client, keep API keys in a secret store, avoid logging tokens or private prompts, and set AI_HIVE_MCP_URL only for a fully trusted endpoint.

Risk: Image or video generation can incur charges, and broad implicit activation could trigger unrelated or premature generation work.

Mitigation: Use the skill only for clearly relevant AI-HIVE animation tasks, query model and price information first, confirm budget and model choices, and require separate confirmation before paid, batch, sending, or public publishing actions.

Risk: Long-running generation tasks may be submitted more than once after a local timeout, causing duplicate work or duplicate cost.

Mitigation: Record task IDs and use ai_hive_get_task to check the original task before retrying or creating a replacement generation request.

Risk: Outputs may unintentionally copy protected IP or use assets without the needed rights.

Mitigation: Use reference works only for structural analysis, maintain a rights checklist for all input materials, and verify originality and public-use permissions before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-091-13cd32b)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Endpoint](https://ai-hive.iclip.cn/api/mcp)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [90s魔法少女动画：原创实施卡](references/original-workflow.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API-Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON work-order files, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AI-HIVE MCP image or video generation only after explicit confirmation; paid generation, batch actions, sending, and public publishing require separate confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
