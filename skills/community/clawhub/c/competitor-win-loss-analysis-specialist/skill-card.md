## Description:

Analyze win/loss data and customer churn interviews to extract competitive positioning insights, battle cards, and messaging frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Go-to-market, sales, marketing, and product teams use this skill to analyze CRM, churn, support, and survey data for competitor win/loss patterns. It produces competitive battle cards, objection patterns, weak spot profiles, positioning guidance, reports, and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive CRM, support, email, survey, Slack, and reporting data.

Mitigation: Install only when operators are authorized for those data sources, use least-privilege read scopes, and redact customer identifiers and deal-sensitive fields before analysis or posting.

Risk: Scheduled reports or Slack/email notifications could disclose deal or customer information to unintended recipients.

Mitigation: Confirm every Slack channel, webhook, email recipient, and report destination before enabling scheduled delivery.

Risk: Competitive intelligence collection may conflict with legal, contractual, or internal policy requirements.

Mitigation: Review external collection practices against legal and internal competitive-intelligence rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/competitor-win-loss-analysis-specialist)
- [ClawHub publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, CSV battle cards, Slack notifications, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on CRM, support, survey, Slack, email, and LLM service credentials configured by the operator.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
