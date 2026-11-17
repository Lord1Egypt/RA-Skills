## Description:

跨境电商产品合规速查 is a Chinese-language agent skill that maps a product category and destination market to structured compliance requirements and an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and compliance reviewers use this skill to get preliminary cross-border ecommerce compliance checklists for supported product categories and destination markets. It helps organize certification, labeling, packaging, testing, restricted-substance, import-document, platform, and special-notice requirements before formal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance requirements may be incomplete or outdated for a specific product, platform, or destination market.

Mitigation: Treat generated reports as preliminary guidance and verify current requirements with official regulators or a qualified compliance provider before export or sale.

Risk: Generated HTML reports may include free-form product names or shared inputs.

Mitigation: Escape inserted values or convert reports to a sanitized format before opening or distributing generated HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/cross-border-ecommerce-compliance)
- [跨境电商产品合规数据库](references/compliance-database.md)
- [Interactive HTML report template](assets/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese-language summary plus generated interactive HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are reference-based preliminary compliance guidance and should be verified against official regulators or qualified compliance providers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
