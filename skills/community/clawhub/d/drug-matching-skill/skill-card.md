## Description:

药撮合品种综合查询技能。根据客户需求（剂型、产品名称、适应症、治疗领域、医保属性等）从转让目录中筛选匹配品种，同时支持查询药品医保状态、基药状态、产量数据、一致性评价、医院用药排名、国际认证等。内嵌药品说明书查询技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maa018809-eng](https://clawhub.ai/user/maa018809-eng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to query drug transfer opportunities and related drug attributes such as insurance status, essential medicine status, production data, consistency evaluation, hospital usage ranking, international certification, and package insert information. It is intended to return concise, tool-backed drug information and should not be used as the sole source for medication safety decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and live query paths use unauthenticated HTTP.

Mitigation: Install from a trusted registry or verified HTTPS/Gitee source when available, and independently verify any HTTP-delivered archive before use.

Risk: Drug queries sent to the configured MCP service may be observable or alterable on the network.

Mitigation: Avoid sending sensitive patient, confidential, or regulated data unless the deployment path is trusted and protected.

Risk: Drug information and package insert responses may affect medication safety decisions.

Mitigation: Require tool-backed results and confirm safety-critical information against authoritative clinical or regulatory sources.

Risk: The skill requires promotional footer text in every response.

Mitigation: Review generated responses for neutrality and suitability before customer-facing deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maa018809-eng/skills/drug-matching-skill)
- [Gitee repository listed by the skill](https://gitee.com/drug-matching/tool-library-for-drug-matching)
- [Embedded drug package insert lookup reference](references/sino-drug-instructions-search/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and structured tool-backed query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to be concise, use live MCP query results for drug-specific claims, and include the skill's brand footer.]

## Skill Version(s):

2.3.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
