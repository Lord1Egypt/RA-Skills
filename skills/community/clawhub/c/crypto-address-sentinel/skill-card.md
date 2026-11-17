## Description:

Monitors wallet balances and on-chain activity across multiple chains, with alerts for balance changes or specified conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiuannnn](https://clawhub.ai/user/zhiuannnn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor cryptocurrency wallet addresses, track portfolios, detect unusual activity, and check airdrop eligibility across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watched wallet addresses can reveal portfolio associations and activity patterns.

Mitigation: Treat configured addresses as sensitive information and share monitoring output only with trusted recipients.

Risk: Webhook alerts may disclose wallet activity or portfolio relationships to the configured endpoint.

Mitigation: Use ALERT_WEBHOOK only with endpoints the user controls or explicitly trusts.

Risk: Short watchlist commands can list or change monitored addresses.

Mitigation: Review command targets before running add, remove, addresses, or balance operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with environment variable settings and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference configured wallet addresses, webhook endpoints, watchlist changes, balances, activity changes, and alert conditions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
