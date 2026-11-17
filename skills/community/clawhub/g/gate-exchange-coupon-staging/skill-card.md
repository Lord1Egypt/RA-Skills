## Description:

Gate coupon and voucher query skill for checking coupon balance, rules, expiry, details, usage history, and acquisition source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Gate Exchange coupon and voucher accounts through read-only Gate MCP coupon queries. It helps list available, expired, or used coupons, inspect details, explain rules, and identify coupon source without performing redemption or trading actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe timestamp-conversion instructions that can push an agent outside the declared MCP-only scope.

Mitigation: Revise timestamp handling to validate integer timestamps and format UTC dates through a safe runtime formatter instead of invoking local shell or programming tools.

Risk: The skill requires Gate API credentials for read-only coupon access.

Mitigation: Use only the configured Gate MCP session, require Coupon:Read permission, and do not ask users to paste API keys or secrets into chat.

## Reference(s):

- [Gate Skills Homepage](https://github.com/gate/gate-skills)
- [Gate Coupon MCP Specification](references/mcp.md)
- [List Coupons](references/list-coupons.md)
- [Coupon Detail](references/coupon-detail.md)
- [Gate Coupon Runtime Rules](references/gate-runtime-rules.md)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown tables and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only coupon query output; may include setup or authentication guidance when the Gate MCP session is unavailable.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter declares 2026.4.8-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
