## Description:

Helps users study publicly available Tongji Zihao content methods, build source-backed method maps, and create original scripts, outlines, visuals, and AI-HIVE execution plans without impersonation or false endorsement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product teams, AI learners, and operators use this skill to analyze public content patterns, prepare traceable research ledgers, and generate original content or strategy-advisor plans through AI-HIVE. It is intended for workflows that require rights checks, source attribution, human review, and explicit boundaries against impersonation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials can be sent to environment-configured endpoints that are not validated.

Mitigation: Prefer OAuth or a managed secret store, avoid broad credentials in shared shells, and set AI_HIVE_MCP_URL or AI_HIVE_BASE_URL only for destinations the user fully trusts.

Risk: AI-HIVE upload and generation tools may expose user materials or create paid tasks.

Mitigation: Confirm model, price, quantity, budget, and upload scope before any generation or media upload; use read-only model listing for initial connection checks.

Risk: Persona-method simulation can be confused with endorsement, authorization, or the subject's own speech.

Mitigation: Require clear disclosure that outputs are AI-assisted method analysis, not Tongji Zihao's views or authorization, and prohibit cloned voice, cloned likeness, fabricated quotes, or false cooperation claims.

Risk: User-provided source materials may include unauthorized paid content, personal data, or trade secrets.

Mitigation: Check access rights and intended use before upload, remove sensitive or unlicensed material, and keep source ledgers with author, date, URL, and permitted use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-simulate-tongji-zihao)
- [AI-HIVE workbench](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)
- [2026 AI channel research source](https://www.jxxy.net/ai/articles/Smartpigai-2085986751987036172/)
- [2026 Chinese AI and creator research source](https://www.jxxy.net/ai/articles/72-chinese-x-bloggers/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON plans, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source attribution, originality boundaries, model and price confirmation steps, task identifiers, and human approval gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
