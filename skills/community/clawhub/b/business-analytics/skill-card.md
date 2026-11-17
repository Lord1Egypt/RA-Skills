## Description:

Turns Excel, CSV, or SQLite business data into an interactive Chinese dashboard with evidence-based findings and suggested actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minibeanai](https://clawhub.ai/user/minibeanai)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and analysts use the skill to reconcile local operating reports, compare revenue, products, customers, and channels, and create a branded offline dashboard for business reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared dashboards may expose business summaries or personal data.

Mitigation: Review generated HTML before sharing; exclude unnecessary personal details and share only within the intended audience.

Risk: An optional branding step processes user-provided images.

Mitigation: Run the logo color script only on images intended for local processing.

Risk: Incomplete or mismatched source data may lead to misleading business conclusions.

Mitigation: Reconcile amounts and periods, state coverage and data limits, and label unsupported explanations as hypotheses.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/minibeanai/skills/business-analytics)
- [Server-resolved source repository](https://github.com/MinibeanAI/business-analytics)
- [Business routing and analysis modes](artifact/references/routing-and-modes.md)
- [Input and channel mapping](artifact/references/input-and-channel-mapping.md)
- [Metrics and periods](artifact/references/metrics-and-periods.md)
- [Dashboard UI and interaction](artifact/references/dashboard-ui.md)
- [Theme and brand adaptation](artifact/references/theme-and-brand.md)
- [Quality checklist](artifact/references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [HTML, Analysis, Guidance]

**Output Format:** [Self-contained offline HTML dashboard with text findings and metric definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters by period, channel, and store when the source data supports them.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
