## Description:

Analyze purchase receipts, order confirmations, travel bookings, subscriptions, and refund emails in a connected Gmail account to estimate spending habits, then compare those habits with cards saved in the Fleece wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers and agents with authorized Gmail and Fleece access use this skill to summarize purchase-email spending patterns, compare observed categories against saved cards, estimate missed rewards, and propose Fleece profile updates that require explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads purchase-related Gmail messages and Fleece wallet data, which can expose sensitive personal spending patterns.

Mitigation: Keep Gmail access read-only, extract only transaction essentials, avoid full message bodies and unrelated personal data, and prefer aggregate reporting.

Risk: Email-derived spending can be incomplete or misleading because receipts may be missing, duplicated, refunded, canceled, or unrelated to card usage.

Mitigation: Report scope, coverage, exclusions, currencies, confidence, and assumptions; distinguish evidence from inference before making recommendations.

Risk: Profile or card-use recommendations could change how the user manages rewards or spending.

Mitigation: Require explicit user confirmation before any Fleece profile updates and review all aggregates and recommendations before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyuan99/skills/fleece-gmail-spend)
- [Publisher profile](https://clawhub.ai/user/chenyuan99)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spending estimates, wallet-fit conclusions, category comparisons, missed-rewards ranges, and user-confirmed profile update commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
