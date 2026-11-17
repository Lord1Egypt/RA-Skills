## Description:

Helps animation, comic, game, original IP, and character-content teams plan and produce original game-demo-style image and video assets through the AI-HIVE MCP workflow, with model and price checks before paid generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to turn a game demo video brief into an original production plan, rights checklist, storyboard, keyframes, animation clips, task records, and acceptance checklist. It is intended for AI-HIVE-assisted content generation where paid generation, batch work, sending, and public publication require separate confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send API credentials to an environment-selected MCP endpoint.

Mitigation: Use the fixed AI-HIVE endpoint, prefer OAuth through the MCP client, and avoid setting AI_HIVE_MCP_URL unless the destination is fully trusted.

Risk: The remote AI-HIVE tool scope includes broad media-generation actions that may create costs or publishable outputs.

Mitigation: Check the model, price, task count, and budget before generation, and require separate confirmation for paid, batch, sending, and public publishing actions.

Risk: Generated game-demo content can accidentally copy protected IP or use media without sufficient rights.

Mitigation: Maintain a rights checklist, use references only for structure or style mechanics, and verify originality, character consistency, scene continuity, and permitted use before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-142-aa975f0)
- [AI-HIVE Workbench](https://ai-hive.iclip.cn/chat)
- [Original Workflow Card](references/original-workflow.md)
- [AI-HIVE MCP Login and Binding Guide](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and optional local JSON work-order files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference AI-HIVE MCP tool calls; paid generation, batch actions, sending, and public publication require separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
