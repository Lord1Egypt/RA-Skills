## Description:

Guides an agent through Amazon product research with live multi-platform validation, 1688 image-based sourcing, USD/CNY conversion, margin screening, WIPO IP checks, and an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachary2024](https://clawhub.ai/user/zachary2024)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace researchers, sourcing teams, and agent operators use this skill to compare Amazon demand signals, supplier matches, gross margin, and IP risk before deciding which products merit further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the agent to copy and reuse SellerSprite session cookies or tokens.

Mitigation: Keep authenticated SellerSprite actions inside the browser session or use an official API key; do not place cookies or tokens in prompts, logs, files, or generated reports.

Risk: The generated HTML report is built from untrusted marketplace data.

Mitigation: Review the report content before sharing or opening it broadly, and treat embedded marketplace values and links as untrusted.

Risk: Product decisions depend on live marketplace, exchange-rate, supplier, and IP-compliance data that can change.

Mitigation: Re-run live checks and manually verify source-labeled values, supplier matches, and HIGH or MEDIUM IP-risk findings before commercial sourcing decisions.

## Reference(s):

- [Amazon Deep Research V4 Skill](https://clawhub.ai/zachary2024/skills/amazon-deep-research-v4)
- [1688 Image Search Strategy](references/1688-image-search.md)
- [Filtering Rules](references/filters.md)
- [HTML Report Template](references/html-template.md)
- [Margin Calculation](references/margin.md)
- [Multi-Platform Data Collection](references/multi-platform.md)
- [SellerSprite API](references/sellersprite-api.md)
- [WIPO IP Compliance Audit](references/wipo-ip.md)
- [AMZScout Product Database](https://amzscout.net/product-database)
- [WIPO Global Brand Database](https://branddb.wipo.int/)
- [SellerSprite Product Research API](https://www.sellersprite.com/v3/api/product-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with code snippets and generated HTML report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source-labeled marketplace research artifacts and an HTML report; live data and authenticated marketplace access may be required.]

## Skill Version(s):

1.0.0-beta.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
