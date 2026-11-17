## Description:

This Chinese-language skill guides brand marketing, ecommerce, agency, retail, and content marketing teams through an AI-HIVE workflow for planning, generating, tracking, and reviewing new-product visual TVC advertising assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketing, ecommerce, agency, retail, and content marketing teams use this skill to create AI-HIVE advertising work orders, storyboards, product key frames, video generation plans, task records, and acceptance checklists for new-product visual TVC campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an untrusted MCP endpoint if the endpoint override is changed.

Mitigation: Prefer OAuth through a trusted MCP client, use the default AI-HIVE MCP endpoint unless a replacement is fully trusted, and keep API keys and tokens out of prompts, logs, screenshots, and repositories.

Risk: Remote MCP tools may upload media or create paid image and video generation tasks.

Mitigation: Use read-only model and task queries first, preserve task IDs for recovery, and require explicit review before paid generation, uploads, bulk operations, sending, or publication.

Risk: Advertising assets may contain unsupported product claims or rights-sensitive reference material.

Mitigation: Maintain a product fact card and asset rights checklist, use references only for structure or mechanics, and review claims, brand consistency, and publication rights before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-105-e3375ff)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [Original Workflow Card](references/original-workflow.md)
- [AI-HIVE MCP Login and Binding Guide](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local work-order JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid generation, uploads, bulk actions, sending, and publication require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
