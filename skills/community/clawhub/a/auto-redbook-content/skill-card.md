## Description:

小红书热点抓取与去AI味改写工具。抓取首页热点→生成去AI味改写提示词→本地存储。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojie66](https://clawhub.ai/user/shaojie66)

### License/Terms of Use:

MIT

## Use Case:

External creators and operators use this skill to collect Xiaohongshu-oriented note data, generate less AI-styled rewrite prompts, and save structured local JSON outputs for review or downstream drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may depend on an OpenClaw-provided Xiaohongshu MCP integration for real network scraping, while the included scripts otherwise produce mock/sample data.

Mitigation: Treat bundled outputs as samples unless a reviewed Xiaohongshu MCP integration is available and approved for the deployment environment.

Risk: XHS_MAX_RESULTS controls requested result count, and the security guidance notes that range validation is not yet clear.

Mitigation: Keep XHS_MAX_RESULTS small until explicit range validation is added and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaojie66/skills/auto-redbook-content)
- [Publisher profile](https://clawhub.ai/user/shaojie66)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [JSON files containing source note fields, metadata, and rewrite prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/xiaohongshu_YYYYMMDD_HHMMSS.json and uses XHS_MAX_RESULTS to control the requested count.]

## Skill Version(s):

2.5.2 (source: frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
