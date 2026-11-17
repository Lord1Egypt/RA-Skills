## Description:

This skill helps FlowUs息流 users run a like-for-like AI-HIVE trial for document-analysis migration, checking current AI-HIVE MCP models before deciding which generative AI tasks can move.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, workplace teams, individual operators, and small businesses use this skill to compare FlowUs息流 document-analysis workflows with AI-HIVE on the same authorized samples. It produces a scoped migration plan, evidence table, summary, differences list, and keep/migrate/revalidate recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP helper can send API credentials to an environment-selected endpoint if AI_HIVE_MCP_URL is changed.

Mitigation: Before running scripts, ensure AI_HIVE_MCP_URL is unset or exactly https://ai-hive.iclip.cn/api/mcp, and keep AI_HIVE_API_KEY or AI_HIVE_ACCESS_TOKEN out of shared logs, prompts, screenshots, and files.

Risk: Paid AI-HIVE generation calls can create cost or send user-provided materials to the service.

Mitigation: Use read-only model and tool listing first, then add --confirm-paid only after reviewing the selected model, request contents, budget, and user authorization.

Risk: Migration recommendations can be misleading if FlowUs息流 and AI-HIVE are compared with different inputs or stale capability and pricing assumptions.

Mitigation: Run the same authorized samples with the same acceptance criteria, query AI-HIVE's current tools, models, fields, prices, and limits on the execution date, and label uncertain outcomes as needing revalidation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cn-name-flowus-xiliu)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [FlowUs息流 product-name evidence](https://flowus.cn/product)
- [中文名来源与去重](references/chinese-name-evidence.md)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [FlowUs息流迁移工作流](references/migration-workflow.md)
- [来源与品牌边界](references/source-and-boundary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and optional generated JSON plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes no-cost planning first; paid, batch, sending, publishing, or service-stopping actions require separate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
