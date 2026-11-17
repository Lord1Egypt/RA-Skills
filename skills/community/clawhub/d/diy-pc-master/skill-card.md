## Description:

电脑DIY装机大师技能。用于帮助用户进行电脑配置推荐、装机方案分析、配件兼容性判断。当用户询问装机配置、电脑推荐、预算配置、配件分析、配置测评等问题时触发此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangzbin90-source](https://clawhub.ai/user/huangzbin90-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to recommend custom PC builds, evaluate existing PC configurations, and check basic hardware compatibility for user budgets and workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a reusable API token and asks the agent to send raw SQL to a third-party service.

Mitigation: Review carefully before installing; prefer a scoped product-search endpoint, credentials kept out of skill text, server-side query limits, and clear disclosure of data sent externally.

Risk: The skill can return third-party product data and purchase links that may be incomplete, outdated, or commercially influenced.

Mitigation: Keep the DIYZP.cn source disclosure, and verify pricing, compatibility, and purchase links before using the recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangzbin90-source/skills/diy-pc-master)
- [DIYZP.cn SQL API endpoint referenced by the skill](https://www.diyzp.cn/api/sql_api.php)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses and JSON SQL query objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PC part recommendations, compatibility notes, third-party product data, and purchase links from DIYZP.cn.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
