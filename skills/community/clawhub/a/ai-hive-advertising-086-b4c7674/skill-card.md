## Description:

Helps brand, ecommerce, agency, store, and content marketing teams plan and produce original toy-style IP advertising assets with AI-HIVE while checking live model availability, cost, rights, task records, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketing, ecommerce, agency, retail, and content marketing teams use this skill to turn product facts, audience goals, and authorized media into ad plans, sample assets, image and video generation steps, multi-ratio deliverables, and compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent to an endpoint selected through environment or launcher configuration.

Mitigation: Prefer OAuth through a trusted MCP client, avoid setting AI_HIVE_MCP_URL, and verify the AI-HIVE MCP endpoint before running the helper with credentials.

Risk: The connected AI-HIVE MCP tools can include paid generation, batch, send, or publishing actions.

Mitigation: Use read-only model and task checks first, review model, quantity, parameters, and budget, and require separate user confirmation before any paid, batch, send, or publish action.

Risk: Long-running generation tasks can be retried accidentally, which may duplicate submissions or cost.

Mitigation: Record task IDs and query the original task before retrying after a timeout.

## Reference(s):

- [Original Workflow Reference](references/original-workflow.md)
- [AI-HIVE MCP Binding Guide](references/mcp-binding.md)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-advertising-086-b4c7674)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON work orders, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE model and price snapshots, task IDs, rights checklists, and acceptance criteria; paid generation and publishing require separate confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
