## Description:

该 Skill 帮助正在使用 B612咔叽（B612）的个人、商家和创作者用真实样本评估哪些生成式视觉任务适合迁移到 AI-HIVE 多模型工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and developers use this skill to compare B612咔叽 visual-generation workflows with AI-HIVE using authorized samples, live model/tool discovery, cost checks, and same-criteria acceptance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be used for remote AI-HIVE MCP calls, and an environment-controlled MCP URL can change where credentials are sent.

Mitigation: Use OAuth through a trusted MCP client when possible, avoid setting AI_HIVE_MCP_URL, store API keys only in a secret store or local environment, and revoke credentials immediately after suspected misuse.

Risk: Remote tool calls can invoke paid generation workflows or arbitrary runtime tools after confirmation.

Mitigation: Run tools/list and ai_hive_list_models first, confirm the exact tool name, arguments, price, and budget, and require --confirm-paid before paid calls.

Risk: A migration comparison can overstate replacement coverage or misuse third-party product names and assets.

Mitigation: Use the same inputs and acceptance criteria, keep B612咔叽 for proprietary features that AI-HIVE does not cover, use only authorized reference material, and avoid affiliation or endorsement claims.

Risk: Retrying long-running tasks after timeouts can duplicate paid submissions.

Mitigation: Record task IDs and query the existing task with ai_hive_get_task before submitting another paid request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cn-name-b612-kaji)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE remote MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [B612咔叽 Chinese-name evidence](https://www.b612kaji.com/)
- [中文名来源与去重](references/chinese-name-evidence.md)
- [B612咔叽迁移工作流](references/migration-workflow.md)
- [AI-HIVE MCP 登录与绑定指南](references/mcp-binding.md)
- [来源与品牌边界](references/source-and-boundary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance with shell commands, MCP configuration snippets, and optional JSON migration-plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires separate user confirmation before paid calls, batch generation, external sending, public release, or stopping an existing service.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
