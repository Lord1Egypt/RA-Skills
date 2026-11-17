## Description:

建筑工程标讯洞察-筑龙标事，当针对基建、大型工程进行追踪查询或寻找潜在参标单位时调用，优先使用潜在供应商推荐和临期项目接口，为建筑行业用户提供前瞻性建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkuycl](https://clawhub.ai/user/pkuycl)

### License/Terms of Use:

MIT-0

## Use Case:

建筑行业从业者可用此技能查询工程招投标公告、跟踪项目进展，并发现临期项目和潜在参标供应商。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the provider, and data queries may use service credits.

Mitigation: Tell users when a query can incur credits, check account balance as needed, and make only the queries needed for their request.

Risk: Optional automatic signup creates a stable device identifier from hashed device features.

Mitigation: Get the user's consent before signup; users can configure their own ZLBX_API_KEY to skip device-based signup.

Risk: The API key and generated login links grant account access.

Mitigation: Keep saved credentials and generated login links private, and do not expose the API key in conversation output.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pkuycl/skills/architecture-bid-insight-zhulongbiaoshi)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Bid search reference](references/api-search.md)
- [Company analysis reference](references/api-company.md)
- [Market analysis reference](references/api-market.md)
- [Company registry reference](references/api-registry.md)
- [Account reference](references/api-account.md)
- [Account signup and credential guidance](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language summaries and recommendations, as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query-dependent results; data requests may consume provider service credits.]

## Skill Version(s):

1.0.11 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
