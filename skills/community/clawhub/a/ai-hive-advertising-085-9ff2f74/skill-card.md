## Description:

Guides agents through an AI-HIVE workflow for one-shot advertising shorts, from audience and rights checks to scripts, keyframes, generation tasks, task tracking, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, e-commerce sellers, agencies, storefront operators, and content marketing teams use this skill to plan and produce one-shot advertising shorts with AI-HIVE. It helps an agent collect audience, channel, budget, rights, model, task, and acceptance evidence before creating or approving generated assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be sent to an endpoint selected through AI_HIVE_MCP_URL.

Mitigation: Use only the official AI-HIVE endpoint, avoid setting AI_HIVE_MCP_URL, and prefer OAuth through the MCP client.

Risk: The MCP helper can invoke tools that upload media or start paid generation tasks.

Mitigation: Keep API keys in a secret store and confirm model, price, budget, uploads, paid generation, batch actions, sending, and publishing before execution.

Risk: Generated advertising outputs can make unsupported claims or use assets without sufficient rights.

Mitigation: Maintain a rights list and fact card, preserve model and task records, and review outputs against the acceptance checklist before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-085-9ff2f74)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [Original workflow card](references/original-workflow.md)
- [AI-HIVE MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON work orders, configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid generation, batch actions, sending, and public publishing require separate confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
