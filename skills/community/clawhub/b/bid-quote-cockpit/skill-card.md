## Description:

Generates self-contained interactive HTML dashboards for comparing multi-vendor, multi-round bid quotes, including total-price ranking, category comparisons, unit-cost analysis, anomaly checks, reconciliation, optional evaluator scoring, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhe223-tech](https://clawhub.ai/user/chenzhe223-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, commercial, and project teams use this skill to turn supplier quote data into an offline HTML decision dashboard for bid comparison, validation, optional scoring, and award-action review. Developers or agents configure JSON inputs and run bundled scripts to generate and verify the dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboards may expose confidential supplier names, prices, evaluator scores, and award recommendations if shared or hosted too broadly.

Mitigation: Default to local or internal distribution, and publish public links only after the data owner explicitly approves external hosting.

Risk: Server security evidence flags a script-injection weakness when untrusted quote text reaches generated HTML.

Mitigation: Sanitize or reject untrusted quotation text and review the generated HTML before sharing it.

Risk: Dashboard rankings and award recommendations can influence procurement decisions.

Mitigation: Treat generated dashboards as decision-support material and keep human commercial review before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzhe223-tech/skills/bid-quote-cockpit)
- [README](artifact/bid-quote-cockpit/README.md)
- [Data contract](artifact/bid-quote-cockpit/references/data-contract.md)
- [Module specification](artifact/bid-quote-cockpit/references/module-spec.md)
- [Score panel contract](artifact/bid-quote-cockpit/references/score-panel-contract.md)
- [Publish and verify guide](artifact/bid-quote-cockpit/references/publish-and-verify.md)
- [Pitfalls and validation notes](artifact/bid-quote-cockpit/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are JSON configuration and self-contained HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard output may embed quote, history, and evaluator-score data into local HTML bytes for consistent offline viewing.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog dated 2026-09-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
