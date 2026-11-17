## Description:

通过理解用户查询、检索并分析相关合金数据（可选通过 MCP 工具），生成专业的合金成分检索回应，并以清晰的筛选、分类与洞察呈现结构化成分表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and technical teams use this skill to search, filter, classify, and analyze metal alloy compositions from user queries, optional alloy data, and optional patent or paper results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may call the configured mace-mcp service to retrieve alloy, patent, or paper data when useful.

Mitigation: Verify that the configured MCP server is trusted before using the skill for research queries.

Risk: Alloy composition results may be incomplete or depend on external source data.

Mitigation: Review cited patent or paper context where available and treat missing composition data as a limitation rather than assuming absent elements are zero.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/alloy-composition-search-zhcn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured alloy composition tables and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and may include cited patent or paper context when evidence is available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
