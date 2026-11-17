## Description:

Helps Fotor懒设计 users compare real visual-design tasks against AI-HIVE models with matching inputs, acceptance criteria, cost checks, and rollback conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, creators, and small businesses use this skill to evaluate whether Fotor懒设计 social-media visual workflows can move to AI-HIVE. It guides a same-input trial, model/tool lookup, scoring, and a migrate/retain/retest decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed MCP access could expose API keys or tokens if the endpoint is changed to an untrusted URL.

Mitigation: Use OAuth or a scoped AI-HIVE API key, keep credentials in a secret store, and do not set AI_HIVE_MCP_URL unless the endpoint is fully trusted.

Risk: Generation, upload, batch, or paid actions may create cost, privacy, or publication exposure.

Mitigation: Require separate user confirmation before any paid, upload, batch, generation, sending, or public-release action.

Risk: Migration conclusions may be misleading without same-input comparison and current AI-HIVE capability checks.

Mitigation: Query current tools, models, fields, prices, and limits on the execution day, then score only matched samples against the documented acceptance criteria.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cn-name-fotor-lansheji)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [Fotor懒设计 Chinese-name evidence](https://www.fotor.com.cn/company/services)
- [中文名来源与去重](references/chinese-name-evidence.md)
- [MCP绑定指南](references/mcp-binding.md)
- [迁移工作流](references/migration-workflow.md)
- [来源与品牌边界](references/source-and-boundary.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration/work-plan examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local migration-plan JSON file and MCP tool-call instructions; paid or generation actions require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
