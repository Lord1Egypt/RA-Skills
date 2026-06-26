## Description: <br>
Gate multi-collateral loan management skill for borrowing crypto against collateral and managing existing loans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users and agent operators use this skill to review multi-collateral loan rates, LTV, quotas, orders, repayments, and collateral adjustments, and to prepare confirmed loan-management actions through Gate MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and execute actions that change real Gate multi-collateral loan positions. <br>
Mitigation: Manually verify every order ID, asset, amount, rate, LTV value, and collateral change before approving any write action. <br>
Risk: Gate credentials with multi-collateral loan permissions can authorize sensitive account operations. <br>
Mitigation: Use the least-privileged Gate credentials available and keep API keys out of prompts, logs, and skill files. <br>
Risk: Using an unintended Gate MCP source could route loan-management requests to the wrong integration. <br>
Mitigation: Confirm the installed Gate MCP server and source before enabling the skill for account operations. <br>
Risk: Loan rates, LTV, quotas, and fixed-rate availability can change before a user approves an action. <br>
Mitigation: Re-check current rate, fixed-rate, quota, LTV, and order state immediately before any confirmed mutation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-exchange-collateralloan) <br>
- [Gate MCP project](https://github.com/gate/gate-mcp) <br>
- [Gate multi-collateral loan API reference](https://www.gate.com/docs/developers/apiv4/zh_CN/#multi-collateral-loan) <br>
- [MCP execution specification](references/mcp.md) <br>
- [MCL MCP tool reference](references/mcl-mcp-tools.md) <br>
- [Collateral loan scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown action drafts, confirmation prompts, query summaries, and MCP-backed operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include order IDs, asset amounts, rates, LTV values, collateral changes, repayment status, and setup guidance; write actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
