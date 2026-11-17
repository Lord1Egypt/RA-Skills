## Description:

Guides agents through an AI-HIVE workflow for producing product advertising short videos, including planning, model routing, draft generation, task tracking, and review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketers, ecommerce sellers, agencies, shops, and content marketing teams use this skill to plan and produce product advertising short videos with AI-HIVE. The workflow emphasizes product facts, material rights, current model and price checks, explicit confirmation for paid or publishing actions, and final acceptance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an unintended MCP endpoint if AI_HIVE_MCP_URL is overridden.

Mitigation: Prefer OAuth in the MCP client, keep AI_HIVE_MCP_URL unset or set exactly to https://ai-hive.iclip.cn/api/mcp, and avoid placing AI_HIVE_ACCESS_TOKEN in a shell.

Risk: Remote generation tools may incur cost or trigger broad content-generation actions.

Mitigation: Call ai_hive_list_models first, verify the model, tool, arguments, price, and budget, and use --confirm-paid only after explicit user approval.

Risk: Advertising output can include unsupported claims or unauthorized product, brand, music, font, image, or video material.

Mitigation: Maintain the fact and rights checklist, use references only for structure or style mechanisms, and review compliance before publication.

Risk: Repeating a timed-out long-running generation task can duplicate work or billing.

Mitigation: Record input hashes and taskId values, then query ai_hive_get_task before retrying or resubmitting generation work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-002-c8910ba)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [MCP Login and Binding Guide](references/mcp-binding.md)
- [Original Workflow Card](references/original-workflow.md)
- [OAuth MCP Config Example](references/mcp-config.example.json)
- [API Key MCP Config Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON work-order files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON work orders; remote AI-HIVE calls require credentialed MCP access and explicit confirmation for paid actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
