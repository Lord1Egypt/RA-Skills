## Description:

AI API Cost Optimizer helps agents audit token and model spend, compare OpenAI, Claude, DeepSeek, and Gemini pricing, and propose lower-cost model, caching, routing, and batch-processing strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caingao](https://clawhub.ai/user/caingao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, and teams using AI APIs use this skill to estimate monthly API spend, choose cost-effective model mixes, and plan token, cache, routing, and batch optimizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing data may become stale or differ by vendor account, region, free tier, or enterprise agreement.

Mitigation: Verify current vendor pricing and applicable discounts before using the skill's estimates for budget decisions.

Risk: Cache examples could retain or expose sensitive data if copied into production without access controls.

Mitigation: Add tenant and user scoping, authorization checks, sensitive-data exclusions, TTLs, and deletion controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caingao/skills/ai-api-cost-optimizer)
- [Publisher profile](https://clawhub.ai/user/caingao)
- [Pricing data](artifact/pricing-data.md)
- [Optimization strategies](artifact/optimization-strategies.md)
- [Routing patterns](artifact/routing-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown reports, comparison tables, checklists, and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses static May 2026 pricing data; readers should verify current vendor prices before making budget decisions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
