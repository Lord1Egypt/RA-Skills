## Description:

This skill guides brand marketers, ecommerce merchants, agencies, stores, and content teams through an AI-HIVE workflow for planning, sampling, generating, tracking, and checking ecommerce advertising visuals, with separate confirmation before paid generation, bulk actions, sending, or publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, agency, store, and content marketing teams use this skill to create ecommerce advertising plans, scripts, product keyframes, videos, aspect-ratio variants, task records, and acceptance checks from product facts and audience insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send credentials to an MCP URL selected through the environment.

Mitigation: Use OAuth through a trusted MCP client when possible, do not set AI_HIVE_MCP_URL unless the destination is fully trusted, and avoid supplying AI_HIVE_ACCESS_TOKEN on the command line.

Risk: The MCP and tool scope is broad and includes uploads, paid generation, bulk actions, sending, and publishing workflows.

Mitigation: Confirm model, cost, destination, and user intent before any upload, generation, bulk action, sending, or publication.

Risk: API keys or OAuth tokens may be exposed through prompts, logs, screenshots, command history, or repository files.

Mitigation: Store secrets only in trusted client secret storage or environment variables, revoke leaked keys immediately, and keep tokens out of skill text, logs, screenshots, and code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-101-d286c12)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Endpoint](https://ai-hive.iclip.cn/api/mcp)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [电商产品视觉全案生成：原创实施卡](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON work orders, model and price snapshots, task records, advertising scripts, visual generation plans, acceptance checklists, and MCP tool-call guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
