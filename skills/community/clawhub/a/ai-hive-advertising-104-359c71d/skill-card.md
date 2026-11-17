## Description:

This skill helps brand, ecommerce, advertising, retail, and content marketing teams plan and produce car or racing promotional shorts with AI-HIVE model routing, work orders, task tracking, and confirmation gates for paid generation or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, ecommerce, retail, and agency users use this skill to turn a car or racing advertising brief into an auditable AI-HIVE production plan, creative direction, scripts, key frames, generated video assets, multi-aspect versions, and acceptance checks. It is designed to require separate confirmation before paid generation, batch actions, sending, or public publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote MCP integration can use AI-HIVE credentials and the helper script can send those credentials to an environment-selected MCP endpoint.

Mitigation: Prefer OAuth in the MCP client, avoid overriding AI_HIVE_MCP_URL, keep API keys in a secret store, and never place tokens in prompts, screenshots, logs, or the repository.

Risk: Image and video generation tools may incur charges or publish/send content if invoked without careful confirmation.

Mitigation: Use ai_hive_list_models for current model and price checks, start with a minimal sample, record task IDs, and require explicit confirmation before paid generation, batch actions, sending, or publishing.

Risk: Advertising outputs can overstate product claims or reuse reference material without sufficient rights.

Mitigation: Maintain a rights checklist and product fact card, use references only for structure or pacing, and verify claims, brand consistency, and publishability before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-104-359c71d)
- [AI-HIVE workbench](https://ai-hive.iclip.cn/chat)
- [Original workflow card](references/original-workflow.md)
- [MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON work orders, MCP configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE MCP tools after user authorization; paid generation, batch actions, sending, and publishing require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
