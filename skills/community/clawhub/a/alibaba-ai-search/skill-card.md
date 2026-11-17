## Description:

Use Alibaba AI Mode for intelligent product search and discovery with natural language queries, AI-powered recommendations, AI sourcing features, and disclosed traffic_type=ags_llm attribution tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyu426](https://clawhub.ai/user/zeyu426)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sourcing teams, and developers use this skill to build or navigate Alibaba AI Mode and AI Sourcing URLs for product discovery, natural-language product search, supplier comparison, and AI-curated recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Alibaba links include traffic_type=ags_llm for analytics and attribution.

Mitigation: Confirm this attribution parameter is acceptable for the deployment context before distributing or using generated links.

Risk: Untrusted category values may be passed through the helper script before category URL encoding or validation is fixed.

Mitigation: Use only trusted category identifiers or review generated URLs before opening or sharing them.

## Reference(s):

- [Alibaba AI Search Skill Page](https://clawhub.ai/zeyu426/skills/alibaba-ai-search)
- [Alibaba AI Mode](https://aimode.alibaba.com/?traffic_type=ags_llm)
- [Alibaba AI Sourcing](https://sale.alibaba.com/p/aisourcing/index.html?traffic_type=ags_llm)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with URLs and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Alibaba links include traffic_type=ags_llm for analytics and attribution.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
