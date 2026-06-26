## Description: <br>
A comprehensive AI marketing partner for DTC ecommerce. Combines multiple diagnostic and optimization skills powered by Attribuly first-party data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexchulee](https://clawhub.ai/user/alexchulee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce teams and marketing operators use this skill to analyze Shopify or WooCommerce performance with Attribuly first-party attribution data, compare ad-platform reporting against attributed revenue, and produce profit-focused optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive store, revenue, funnel, Google Ads, and Meta Ads data through an Attribuly API key. <br>
Mitigation: Install only for intended Attribuly-connected workspaces and prefer a least-privilege or read-only API key when available. <br>
Risk: API-key handling guidance may expose secrets if keys are printed, stored in shell history, or embedded in Docker or service files. <br>
Mitigation: Use a secret manager or protected environment configuration and avoid logging or sharing the full ATTRIBULY_API_KEY value. <br>
Risk: Automatic triggers and chained reports may run analyses over connected ad and store accounts without enough operator context. <br>
Mitigation: Confirm scheduled or chained report runs and review account, date range, and attribution-model assumptions before relying on the output. <br>
Risk: Budget, pause, bid, and scaling recommendations could materially affect advertising spend if applied directly. <br>
Mitigation: Require human review and approval before changing budgets, bids, campaign status, or audience targeting. <br>


## Reference(s): <br>
- [Attribuly homepage](https://attribuly.com) <br>
- [Attribuly DTC skills source](https://github.com/Attribuly-US/ecommerce-dtc-skills) <br>
- [Attribuly ClawHub listing](https://clawhub.ai/alexchulee/attribuly) <br>
- [Weekly marketing performance reference](references/weekly-marketing-performance.md) <br>
- [Daily marketing pulse reference](references/daily-marketing-pulse.md) <br>
- [Google Ads performance reference](references/google-ads-performance.md) <br>
- [Meta Ads performance reference](references/meta-ads-performance.md) <br>
- [Budget optimization reference](references/budget-optimization.md) <br>
- [Attribution discrepancy reference](references/attribution-discrepancy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, recommendations, API-derived metrics, and occasional shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include budget, bid, pause, and scaling recommendations that require human approval before execution.] <br>

## Skill Version(s): <br>
2026.4.8 (source: server release metadata; artifact frontmatter version 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
