## Description:

AstrMap VOC helps e-commerce sellers improve products and research markets by analyzing Amazon reviews, surfacing recurring issues, and tracking review trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkbayes](https://clawhub.ai/user/sparkbayes)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers use this skill to review Amazon customer feedback, identify recurring product issues and unmet needs, and inform product improvements, new-product development, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is sent to AstrMap for authentication and could be exposed if shared or embedded in commands or scripts.

Mitigation: Store the key in the CUSTOMER_INSIGHTS_API_KEY environment variable, keep it private, and use a read-only key when only viewing existing results.

Risk: Creating collection or analysis tasks can consume account credits.

Mitigation: Check the credit cost and obtain the user's confirmation before starting any paid task or analysis.

Risk: The browser extension used for collection can access data on logged-in Amazon pages.

Mitigation: Verify the download comes from AstrMap over HTTPS, review requested extension permissions, and use a dedicated buyer account in an isolated browser profile separate from seller accounts.

Risk: The API client depends on the third-party Requests package.

Mitigation: Install a reviewed Requests version from a trusted package source.

## Reference(s):

- [AstrMap VOC on ClawHub](https://clawhub.ai/sparkbayes/skills/astrmap-voc)
- [AstrMap API Reference](references/api_reference.md)
- [AstrMap Browser Extension Security Guide](references/security.md)
- [AstrMap Website](https://www.astrmap.com)
- [AstrMap Web App](https://app.astrmap.com/)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance]

**Output Format:** [Structured review-analysis results and natural-language guidance, commonly returned as JSON by the API client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include review summaries, issue and category frequencies, representative reviews, product details, and review trends.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
