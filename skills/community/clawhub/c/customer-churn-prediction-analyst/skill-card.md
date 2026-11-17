## Description:

Analyzes customer behavior patterns to predict churn risk across Stripe, Shopify, and SaaS platforms, identify at-risk accounts, recommend interventions, and track win-back success.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success, growth, and operations teams use this skill to prioritize retention work, produce risk-ranked churn reports, draft win-back campaigns, and monitor retention ROI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad customer and payment data access.

Mitigation: Use scoped or test API keys where possible, limit data collection to fields needed for churn analysis, and review permissions before production use.

Risk: Customer data may be sent to OpenAI, Slack, or custom SaaS endpoints.

Mitigation: Confirm data handling for each destination, minimize or redact sensitive customer identifiers, and verify notification contents before enabling integrations.

Risk: Scheduled analysis or campaign workflows could run before approval boundaries are clear.

Mitigation: Keep interventions and account changes behind human approval, and avoid scheduled runs until notification, storage, and approval workflows are reviewed.

Risk: Churn predictions can produce false positives or misleading account priorities.

Mitigation: Manually spot-check high-value or high-risk accounts before outreach and treat scores as decision support rather than deterministic outcomes.

## Reference(s):

- [Customer Churn Prediction Analyst on ClawHub](https://clawhub.ai/ncreighton/skills/customer-churn-prediction-analyst)
- [Project homepage](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON examples with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces risk reports, intervention playbooks, campaign templates, dashboard summaries, setup commands, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
