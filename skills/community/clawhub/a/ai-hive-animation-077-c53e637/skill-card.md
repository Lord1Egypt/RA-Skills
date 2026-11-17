## Description:

This skill helps creative teams plan and produce an original open-world urban mission-style game trailer workflow with AI-HIVE image and video tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External animation, comics, game, original IP, and character-content teams use this skill to create a planned, reviewable AI-HIVE production flow for original trailer concepts, storyboards, key frames, video clips, task records, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials could be sent to an untrusted MCP endpoint if AI_HIVE_MCP_URL is changed.

Mitigation: Use OAuth through a trusted MCP client when possible, avoid command-line access tokens, and only set AI_HIVE_MCP_URL for destinations the installer fully trusts.

Risk: Remote tool calls can create uploads or paid image and video generation tasks.

Mitigation: Confirm the exact tool, model, parameters, price, and budget before generation or upload, and use ai_hive_list_models and ai_hive_get_task for non-billable checks where possible.

Risk: Trailer generation can accidentally use unlicensed characters, logos, music, portraits, or source media.

Mitigation: Keep a rights checklist, separate owned or licensed material from reference-only material, and require review before public publishing.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/wubin1836/skills/ai-hive-animation-077-c53e637)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Login and Binding Guide](references/mcp-binding.md)
- [Original Workflow Card](references/original-workflow.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API-Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local JSON work-order files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The planning helper can produce a local non-billable work order; AI-HIVE generation, upload, batch, send, and publish actions require separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
