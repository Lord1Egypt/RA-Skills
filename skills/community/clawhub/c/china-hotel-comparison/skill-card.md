## Description:

China Hotel Comparison helps agents compare hotels across major Chinese travel platforms, analyze total costs and packages, and provide personalized booking recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to search for hotels in China, compare options across Meituan, Qunar, Ctrip, Fliggy, and Tuniu, and produce booking recommendations with price, package, location, cancellation, and suitability analysis.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Persistent personalization and family sharing could expose travel searches, decision history, inferred preferences, or shared household data.

Mitigation: Require explicit opt-in, collect only necessary data, keep personal and household data separated, and provide review, export, and deletion controls before deployment.

Risk: Embedded raw web-fetch text could cause an unsolicited web request.

Mitigation: Remove raw web-fetch lines from the artifact or require explicit user confirmation before any live web access.

Risk: Hotel prices, package values, cancellation terms, and availability may be stale or inaccurate.

Mitigation: Verify live prices and policies against the booking platform or official provider at recommendation time and show the source and timestamp for critical values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengjianli0721/skills/china-hotel-comparison)
- [README](artifact/README.md)
- [Search Strategy](artifact/search-strategy.md)
- [Price Calculation](artifact/price-calculation.md)
- [Package Value Analysis](artifact/package-value-analysis.md)
- [Multi-User Management](artifact/multi-user-management.md)
- [User Profiles](artifact/user-profiles.md)
- [Personalized Recommendation](artifact/personalized-recommendation.md)
- [Shanghai Disney Resort Tickets](https://www.shanghaidisneyresort.com/tickets/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with comparison tables and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel recommendations are expected to include at least five options with price comparisons, cost breakdowns, pros and cons, audience fit, and booking guidance.]

## Skill Version(s):

1.4.0 (source: evidence release.version, artifact _meta.json, and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
