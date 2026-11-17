## Description:

Queries Gate Exchange coupon and voucher balances, rules, expiry, status, and acquisition source through read-only coupon tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and agents use this skill to inspect account coupons and vouchers, including available coupons, expired or used coupons, detailed rules, expiry timing, and source information. It is intended for read-only account inquiry through a configured Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gate API credentials may grant more account access than this skill needs if they are over-scoped.

Mitigation: Use a Gate API key scoped to Coupon:Read only, and avoid trading or transfer permissions.

Risk: API secrets could be exposed if they are pasted into chat.

Mitigation: Use the configured local MCP session and environment variables; do not paste API secrets into conversation text.

Risk: Coupon details can include account-specific financial incentive information.

Mitigation: Keep responses limited to the requested coupon inquiry and use only the documented read-only coupon tools.

Risk: Incorrect coupon type mapping can misstate voucher behavior or rules.

Mitigation: Map each returned coupon_type to the documented display name exactly, especially position_voucher and contract_bonus.

## Reference(s):

- [Gate Coupon MCP Specification](references/mcp.md)
- [List Coupons Workflow](references/list-coupons.md)
- [Coupon Detail Workflow](references/coupon-detail.md)
- [Gate Coupon Runtime Rules](references/gate-runtime-rules.md)
- [Gate Skills Homepage](https://github.com/gate/gate-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables, detail cards, and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gate coupon queries; no coupon redemption, trading, transfer, or write actions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
