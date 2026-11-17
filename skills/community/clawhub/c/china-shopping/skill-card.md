## Description:

Recommend suitable Chinese shopping platforms for a user-provided product type, product name, or shopping need.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to choose suitable Chinese e-commerce platforms for a product category, product name, or shopping intent. It supports offline, category-based recommendations and practical caveats for platform fit, seller trust, authenticity, and delivery considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may be stale or incomplete because the skill uses bundled static data.

Mitigation: Use the output as category guidance only, and verify current prices, availability, seller reputation, delivery terms, and listing safety through live sources before purchasing.

Risk: The skill does not verify sellers, official stores, authenticity, or product safety for a specific listing.

Mitigation: Prefer official stores or trusted sellers and review platform reputation signals before relying on a recommendation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/china-shopping)
- [Category Guide](references/category-guide.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown recommendation sections, with optional Chinese CLI text or JSON when the local Python tool is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled static category and product-mapping data; does not perform live browsing, real-time price checks, or seller verification.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
