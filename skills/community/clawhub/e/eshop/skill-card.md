## Description:

eShop routes shopping and food-delivery requests across supported merchants and platforms to help users search products, claim coupons, place or manage orders, and track delivery or order status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fireium](https://clawhub.ai/user/fireium)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-assistant agents use eShop to interpret Chinese shopping or delivery requests, route them to supported merchant or platform instructions, and assist with product search, coupon handling, order creation or cancellation, and order tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or close shopping and delivery orders, which may cause charges or account changes.

Mitigation: Require explicit user confirmation before order creation, order cancellation, coupon claiming, payment-link handoff, or use of saved account data.

Risk: The skill may use shopping tokens, saved addresses, coupons, points, and order-management data.

Mitigation: Keep tokens out of logs and responses, display only the minimum account details needed for the task, and let the host handle sensitive credentials.

Risk: Configurable MCP endpoint variables could route account or order actions to an untrusted service.

Mitigation: Use only trusted MCP endpoint URLs and reject or review endpoint overrides before running account, order, or payment-related actions.

## Reference(s):

- [ClawHub eShop skill page](https://clawhub.ai/fireium/skills/eshop)
- [fireium ClawHub publisher profile](https://clawhub.ai/user/fireium)
- [McDonald's China MCP endpoint](https://mcp.mcd.cn)
- [Luogang MCP endpoint](https://yuju-mcp.wxhoutai.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Chinese conversational text with Markdown lists, tables, and inline shell-command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured MCP endpoints and user/account tokens for order and account actions; order and cancellation actions should require explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
