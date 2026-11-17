## Description:

Helps marketing, ecommerce, agency, retail, and content teams plan and run an AI-HIVE workflow for multi-grid advertising videos, including audience planning, rights checks, scripts, key frames, generated video, variant outputs, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and content-production users can use this skill to turn a multi-grid video advertising brief into an auditable AI-HIVE production workflow. It emphasizes model and price lookup before generation, explicit confirmation before paid or public actions, and review of facts, rights, task records, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials could be sent to an untrusted MCP endpoint if the endpoint is overridden.

Mitigation: Use OAuth through https://ai-hive.iclip.cn/api/mcp where possible and set AI_HIVE_MCP_URL only after independently trusting the endpoint.

Risk: The helper can invoke broader MCP tools than the workflow clearly scopes.

Mitigation: Review requested tool calls before execution and start with read-only model or task queries before any generation workflow.

Risk: Paid generation, upload, batch, sending, or publishing actions can create cost or public exposure.

Mitigation: Require explicit user confirmation before paid generation, uploads, batch operations, sending, or public publishing.

Risk: Advertising outputs can contain unsupported claims, rights issues, or overpromises.

Mitigation: Maintain a product fact card and materials rights list, then check brand consistency, visible claims, permissions, and acceptance criteria before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-060-c891850)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [AI-HIVE MCP login and binding guide](references/mcp-binding.md)
- [Original workflow implementation card](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON work orders and AI-HIVE task records when the agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
