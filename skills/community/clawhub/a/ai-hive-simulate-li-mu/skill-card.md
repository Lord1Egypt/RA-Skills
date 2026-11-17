## Description:

Researches Li Mu's public content methods, builds source-tracked method maps, and helps agents produce original scripts, visual plans, short-video plans, and AI-HIVE execution plans without impersonating Li Mu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product teams, AI learners, and technology practitioners use this skill to analyze public Li Mu content patterns, organize authorized materials into a source-tracked methodology knowledge base, and produce original content plans through AI-HIVE. It is also used to plan AI-HIVE model, media, and MCP workflows with human review before paid or public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an environment-configured destination if helper scripts run with untrusted AI_HIVE_BASE_URL or AI_HIVE_MCP_URL values.

Mitigation: Use OAuth through the official AI-HIVE MCP URL where possible, keep API keys in a trusted secret store, and run helper scripts only from trusted shells or launch profiles with reviewed environment variables.

Risk: Media generation, ecommerce, advertising, or bulk tasks may upload user content or incur charges.

Mitigation: Confirm the model, price snapshot, quantity, budget, and upload contents before creating generation tasks, then track task IDs instead of blindly resubmitting after timeouts.

Risk: Outputs about Li Mu could be mistaken for impersonation, endorsement, cloned identity, fabricated quotation, or copied protected expression.

Mitigation: Use public or authorized materials, require original wording, avoid voice or face cloning, label outputs as AI methodology analysis, and perform human review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-simulate-li-mu)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [AI-HIVE MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API-key MCP configuration example](references/mcp-config-api-key.example.json)
- [2026 AI channel research source](https://www.jxxy.net/ai/articles/Smartpigai-2085986751987036172/)
- [Knowledge-payment and personal-IP industry source](https://www.36kr.com/p/1881869085773187)
- [AI influencer research source](https://x.feedspot.com/artificial_intelligence_twitter_influencers/)
- [2026 Chinese AI and startup creator source](https://www.jxxy.net/ai/articles/72-chinese-x-bloggers/)
- [AIGC creator ranking source](https://www.sohu.com/a/973107895_122268060)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON execution plans, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source ledgers, methodology maps, originality checks, AI-HIVE MCP setup steps, model and price snapshots, task IDs, and human approval gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
