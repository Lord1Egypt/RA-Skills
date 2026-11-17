## Description:

核对 Amazon 商品页承诺与评论中的真实使用体验，识别有评论证据支持的消费者预期差距。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon operators and product analysts use this skill to compare product page promises with review evidence and prepare a scoped expectation-gap audit. It is not for legal compliance review or unrestricted listing copywriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broader operations may spend credits during actions described as previews.

Mitigation: Prefer a corrected audit-only package that fixes preview charging; if proceeding, configure the account to ask before every charge.

Risk: Broader tools can enable ongoing paid collection.

Mitigation: Approve recurring collection separately, and review existing schedules and competitor subscriptions.

## Reference(s):

- [ClawHub release](https://clawhub.ai/funewa/skills/customer-gap)
- [Operation workflow](references/operation-workflow.md)
- [ARI CLI and API reference](references/reference.md)
- [ARI operations](https://ari.funewa.com/zh/operations)
- [ARI reports](https://ari.funewa.com/zh/reports)
- [ARI billing](https://ari.funewa.com/zh/billing)
- [ARI API key settings](https://ari.funewa.com/zh/account?ui=d47626f#api-keys)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Concise text or Markdown audit summary grounded in review evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.5.3 (source: release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
