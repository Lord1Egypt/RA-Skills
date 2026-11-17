## Description:

Helps directors, cinematographers, creative teams, and content creators plan and produce AI-HIVE image and video assets for gaze-oriented long-take cinematic shorts, with model lookup, work orders, task tracking, and confirmation gates before paid generation or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and creative teams use this skill to turn a short-film brief into an AI-HIVE production plan, rights checklist, model and pricing snapshot, keyframe or video generation workflow, task record, and acceptance checklist. It is intended for original cinematic content workflows where paid generation, batch actions, sending, and public publishing require separate confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to a nonstandard MCP URL if the helper script is run with an overridden endpoint.

Mitigation: Use the fixed AI-HIVE MCP endpoint, avoid setting AI_HIVE_MCP_URL with real credentials, and prefer managed OAuth or scoped, revocable API keys.

Risk: Media generation, upload, batch, send, or publishing actions may have cost or publication impact.

Mitigation: Confirm model, price, quantity, upload inputs, paid generation, batch actions, sending, and public publishing before running those actions.

Risk: Reference materials, brands, likenesses, music, fonts, or source media may introduce rights or authenticity issues.

Mitigation: Maintain a rights checklist, use original or authorized assets, preserve task records, and review acceptance criteria before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-cinema-027-557880f)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Endpoint](https://ai-hive.iclip.cn/api/mcp)
- [MCP 登录与绑定指南](references/mcp-binding.md)
- [原创实施卡](references/original-workflow.md)
- [OAuth MCP Config Example](references/mcp-config.example.json)
- [API Key MCP Config Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and optional local JSON work-order files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local non-billable work-order JSON; AI-HIVE generation tasks require user confirmation before paid, batch, send, or publish actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
