## Description:

Amazon Selection Agent helps experienced Amazon sellers research product opportunities through market scanning, competitor analysis, FBA profit modeling, and keyword discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Experienced Amazon sellers use this skill to evaluate categories, ASINs, keywords, and product links before sourcing or listing decisions. It supports category exploration, product deep dives, competitor review mining, FBA fee and profit modeling, keyword opportunity analysis, and final go/no-go recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may include private Seller Central data, supplier terms, or other confidential inputs in saved Markdown reports if the user provides them.

Mitigation: Use public product and category data by default, and avoid entering Seller Central data, API keys, or confidential supplier details unless the workspace and report are approved for that information.

Risk: Product, fee, and market estimates can become stale or be wrong when sourced from public web pages or third-party tools.

Mitigation: Cross-check important metrics against current Amazon pages and professional seller tools before making purchasing or launch decisions.

Risk: Marketplace research can raise restricted-product, brand, patent, or category-compliance issues.

Mitigation: Run independent legal, intellectual-property, and Amazon category-compliance review before sourcing or listing a recommended product.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shylamb-token/skills/amazon-selection-agent)
- [Data sources and search strategy](artifact/references/data-sources.md)
- [Amazon FBA fees and profit calculation reference](artifact/references/fba-fees.md)
- [Product research report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown report with tables, cited data notes, FBA calculations, sensitivity analysis, and a decision rating]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a local Markdown report; analysis relies on public web sources and user-provided product or category inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
