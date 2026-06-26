## Description: <br>
Gate coupon and voucher query skill for checking coupon balances, details, rules, expiry, and acquisition source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate Exchange users use this skill to query their own coupon and voucher inventory, inspect details, review usage rules, and understand coupon source information through a configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gate API credentials may expose account-specific coupon metadata if installed with broader account permissions. <br>
Mitigation: Use an API key restricted to Coupon:Read and avoid trading, withdrawal, or account-write scopes. <br>
Risk: Coupon metadata is account-specific and may be shown in the chat response. <br>
Mitigation: Run the skill only in trusted sessions and ask for coupon data only when that disclosure is intended. <br>
Risk: Coupon type confusion could produce misleading guidance, especially between position vouchers and futures bonuses. <br>
Mitigation: Follow the bundled coupon type mapping exactly and preserve returned status and time fields without inventing availability. <br>
Risk: The skill depends on a configured Gate MCP session and cannot complete lookups when authentication or coupon tools are unavailable. <br>
Mitigation: Stop and provide setup or authentication guidance when the Gate MCP coupon endpoints are missing or credentials are not configured. <br>


## Reference(s): <br>
- [Gate Coupon Assistant](SKILL.md) <br>
- [Coupon Detail](references/coupon-detail.md) <br>
- [Gate Coupon Runtime Rules](references/gate-runtime-rules.md) <br>
- [List Coupons](references/list-coupons.md) <br>
- [Gate Coupon MCP Specification](references/mcp.md) <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables with account-specific coupon fields returned from read-only Gate MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gate MCP session with GATE_API_KEY and GATE_API_SECRET using Coupon:Read permission.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
