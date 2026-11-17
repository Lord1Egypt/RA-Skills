## Description:

Search, compare, and research products from Argos.co.uk with natural language queries

This skill is ready for commercial/non-commercial use.

## Publisher:

[notsurewhoisthis](https://clawhub.ai/user/notsurewhoisthis)

### License/Terms of Use:

MIT

## Use Case:

External shoppers and product researchers use this skill to search Argos.co.uk, inspect product details, compare products, and summarize customer reviews from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill through an npx command can run package-manager code from the selected registry.

Mitigation: Install only from a trusted registry, avoid administrator privileges, and pin the installer version or use a reviewed local install path when possible.

Risk: Optional local caching may retain product data when caching is enabled.

Mitigation: Keep caching disabled unless needed, set a short cache TTL, and avoid storing sensitive user-specific shopping context in cached files.

Risk: Real-time product details such as price, stock, delivery, and reviews can change after the skill reports them.

Mitigation: Fetch current Argos product pages when answering and encourage users to verify price and availability on Argos before purchase.

## Reference(s):

- [Argos](https://www.argos.co.uk)
- [ClawHub Skill Page](https://clawhub.ai/notsurewhoisthis/skills/argos-product-research)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown tables and concise prose summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Argos product links, prices, availability, ratings, comparisons, recommendations, and review themes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
