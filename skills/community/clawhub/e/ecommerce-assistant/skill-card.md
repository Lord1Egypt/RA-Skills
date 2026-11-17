## Description:

E-commerce product research, competitor analysis, and price monitoring for Amazon, Shopify, and other platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhldolike](https://clawhub.ai/user/lhldolike)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, sellers, and researchers use this skill to research Amazon products, analyze Shopify competitor stores, monitor prices, and generate product reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock or demo Amazon search and price tracking data could be mistaken for current market research.

Mitigation: Remove or clearly label mock/demo behavior and require validated live data sources before using results for business decisions.

Risk: Shopify analysis can fetch arbitrary store URLs supplied by the user.

Mitigation: Analyze only trusted store URLs until URL validation, allowlisting, or other input controls are added.

Risk: Running the scripts can create local watchlist, price history, report, or output files.

Mitigation: Disclose generated file paths, review outputs before sharing, and run the skill in an isolated workspace when testing.

## Reference(s):

- [Amazon API Guide](artifact/references/amazon-api.md)
- [Shopify API Guide](artifact/references/shopify-api.md)
- [ClawHub Skill Page](https://clawhub.ai/lhldolike/skills/ecommerce-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus script outputs in table, JSON, CSV, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local watchlist and price history JSON under ~/.ecommerce-assistant and optional user-named output files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
