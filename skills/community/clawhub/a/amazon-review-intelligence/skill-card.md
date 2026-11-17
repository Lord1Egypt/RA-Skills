## Description:

Analyzes collected Amazon reviews to surface customer pain points, buying motivations, trends, competitor differences, and listing or PPC keyword opportunities, with optional ongoing monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and product operators use ARI to analyze collected reviews, compare competitors, improve listings, and track review or product changes over time.

### Deployment Geography for Use:

Global (Amazon US, UK, Germany, Japan, Canada, France, Spain, and Italy marketplaces)

## Known Risks and Mitigations:

Risk: Some analyses can spend account credits without a per-request price approval under account auto-confirm rules, and recurring collection or product watches can create ongoing costs.

Mitigation: Before analysis, explicitly set spending confirmation to off; use quote for price-only requests. Approve recurring costs separately and review existing schedules and watches, since changing confirmation settings does not cancel monitoring.

## Reference(s):

- [ARI API and command reference](references/reference.md)
- [ARI monitor center](https://ari.funewa.com/zh/monitor)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ARI report center](https://ari.funewa.com/zh/reports)
- [ARI Review Intelligence on ClawHub](https://clawhub.ai/funewa/skills/amazon-review-intelligence)

## Skill Output:

**Output Type(s):** [Analysis, Recommendations, Text, Markdown, CSV, HTML]

**Output Format:** [Concise text or Markdown analysis and reports, with optional CSV, Markdown, or HTML exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on reviews collected by ARI and should state their sample and date coverage; they do not guarantee coverage of all Amazon reviews.]

## Skill Version(s):

1.5.3 (source: release evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
