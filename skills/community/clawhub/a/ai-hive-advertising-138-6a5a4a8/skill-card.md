## Description:

Helps brand, ecommerce, advertising, retail, and content marketing teams plan and produce AI-HIVE font-motion advertising assets from audience insight, product facts, model availability, pricing, sample generation, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and commerce users use this skill to turn a font-motion advertising brief into a rights-aware creative plan, model route, sample, generated image/video assets, task record, and acceptance checklist. Developers and agent operators can also use its MCP binding notes and helper scripts to connect AI-HIVE safely before running generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send API credentials to a configurable MCP URL.

Mitigation: Use OAuth or an API key only with the official AI-HIVE endpoint, and do not accept AI_HIVE_MCP_URL values from untrusted projects or wrappers.

Risk: Remote AI-HIVE tools include broad generation, upload, batch, sending, publishing, and potentially paid actions.

Mitigation: Require explicit confirmation before paid, batch, sending, upload, or publishing actions; query model and pricing information before generation.

Risk: Advertising outputs can misuse third-party assets or make unsupported product claims.

Mitigation: Maintain a rights checklist and product fact card, and verify claims, licensing, brand constraints, and acceptance criteria before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-138-6a5a4a8)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP Login and Binding Guide](references/mcp-binding.md)
- [Original Font-Motion Advertising Workflow](references/original-workflow.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local JSON work-order files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may call remote AI-HIVE MCP tools after explicit user confirmation; the planning helper writes a local non-billable work-order JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
