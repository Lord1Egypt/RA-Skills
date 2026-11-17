## Description:

A comprehensive AI marketing partner for DTC ecommerce that combines multiple diagnostic and optimization skills powered by Attribuly first-party data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexchulee](https://clawhub.ai/user/alexchulee)

### License/Terms of Use:

MIT-0

## Use Case:

External DTC ecommerce merchants, marketers, and developers use this skill to analyze Shopify and WooCommerce marketing performance, reconcile ad-platform reporting with Attribuly first-party data, and generate optimization guidance for spend, audiences, creatives, funnels, and landing pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can expose the sensitive ATTRIBULY_API_KEY if users paste real keys into shell history, profile files, Compose files, screenshots, or support logs.

Mitigation: Use a secret manager or masked OpenClaw secret facility, avoid storing keys in logs or shell profiles, and rotate the key if exposure is suspected.

Risk: Daily, weekly, and threshold-triggered analyses may run automatically outside the user's intended workspace or account scope.

Mitigation: Confirm automatic analyses are opt-in, scoped to the intended workspace and account, and reviewed before budget or campaign changes are applied.

Risk: Marketing recommendations based on attribution data can be incorrect or misleading if source data, attribution model, date range, or account selection is wrong.

Mitigation: Verify account IDs, date ranges, response codes, and platform-vs-Attribuly comparisons before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexchulee/skills/attribuly)
- [Attribuly homepage](https://attribuly.com)
- [Weekly Marketing Performance](references/weekly-marketing-performance.md)
- [Daily Marketing Pulse](references/daily-marketing-pulse.md)
- [Google Ads Performance](references/google-ads-performance.md)
- [Meta Ads Performance](references/meta-ads-performance.md)
- [Google Creative Analysis](references/google-creative-analysis.md)
- [Meta Creative Analysis](references/meta-creative-analysis.md)
- [Budget Optimization](references/budget-optimization.md)
- [Audience Optimization](references/audience-optimization.md)
- [Bid Strategy Optimization](references/bid-strategy-optimization.md)
- [Funnel Analysis](references/funnel-analysis.md)
- [Landing Page Analysis](references/landing-page-analysis.md)
- [Attribution Discrepancy Analysis](references/attribution-discrepancy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and recommendations with occasional shell commands, configuration snippets, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include multilingual analysis, metric tables, diagnostics, and human-approved optimization recommendations.]

## Skill Version(s):

2026.4.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
