## Description:

Analyze customer usage, support, billing, and engagement signals to score churn risk and recommend retention actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Customer success and revenue teams use this skill to prioritize at-risk accounts, understand revenue exposure, and plan retention outreach. It can work from CSV exports, CRM or billing data, support logs, usage analytics, or qualitative account descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer, support, billing, and revenue inputs may include confidential or regulated information.

Mitigation: Use sanitized exports where possible and provide only the data needed for churn assessment.

Risk: Retention recommendations may be incomplete or unsuitable if treated as automatic customer-action instructions.

Mitigation: Use the report as decision support and have customer success or account owners review actions before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-churn-analyzer)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)
- [AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown retention report with ranked churn-risk accounts, recommended actions, revenue-at-risk estimates, and a 30/60/90 day calendar]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weighted risk scores from 0 to 100 and account categories from Thriving to Critical.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
