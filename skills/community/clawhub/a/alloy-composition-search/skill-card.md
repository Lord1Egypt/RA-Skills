## Description:

Generate professional alloy composition search responses by interpreting user queries, retrieving and analyzing relevant alloy data (optionally via MCP tools), and presenting structured composition tables with clear filtering, classification, and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and materials engineers use this skill to search, filter, classify, and analyze metal alloys by composition, application context, and supporting patent or paper evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query an external MCP service for alloy substances, documents, and composition data.

Mitigation: Confirm what data the MCP server receives and returns before using the skill with proprietary research or sensitive material.

Risk: Alloy composition results may be incomplete or only partially matched to the user's constraints.

Mitigation: Prefer document-backed composition data and clearly label exact matches, partial matches, missing data, and limitations in the response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/alloy-composition-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown responses with alloy summaries, composition tables, match summaries, detailed notes when useful, and concise insights.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document-backed references, exact versus partial match indicators, composition units, and limitations when data is incomplete.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
