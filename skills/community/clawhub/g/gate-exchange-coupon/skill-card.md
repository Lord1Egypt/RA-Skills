## Description: <br>
Gate coupon and voucher query skill for coupon balance, rules, expiry, source, list, and detail requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users use this skill to inspect coupon and voucher availability, details, usage rules, expiry, and source through a locally configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a Gate account through a local MCP session and depends on API credentials. <br>
Mitigation: Use a Gate API key limited to Coupon:Read, do not grant trading, transfer, withdrawal, or redemption permissions, and do not paste API secrets into chat. <br>
Risk: Coupon data may include account-specific balances, IDs, expiry times, and source information. <br>
Mitigation: Keep responses scoped to the current request and avoid exposing API secrets or unrelated account data. <br>


## Reference(s): <br>
- [Gate Exchange Coupon on ClawHub](https://clawhub.ai/gate-exchange/gate-exchange-coupon) <br>
- [Publisher Profile](https://clawhub.ai/user/gate-exchange) <br>
- [ClawHub Metadata Homepage](https://github.com/gate/gate-skills) <br>
- [Coupon Detail Reference](references/coupon-detail.md) <br>
- [Gate Runtime Rules](references/gate-runtime-rules.md) <br>
- [List Coupons Reference](references/list-coupons.md) <br>
- [MCP Execution Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and tables backed by read-only MCP coupon queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Gate MCP configuration with GATE_API_KEY and GATE_API_SECRET scoped to Coupon:Read.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
