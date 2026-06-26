## Description: <br>
Gate unified account operations skill for account equity, margin borrowing, repayment, leverage modes, collateral settings, and related unified-account checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Gate unified-account status, limits, loan records, borrow rates, and to prepare confirmed borrow, repay, mode, leverage, or collateral actions through a configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with borrow, repay, leverage, mode, and collateral changes that may affect margin exposure or liquidation risk. <br>
Mitigation: Use a dedicated, tightly scoped Gate API key and review each Action Draft before giving explicit confirmation. <br>
Risk: A misconfigured or untrusted Gate MCP server could expose account credentials or route account actions incorrectly. <br>
Mitigation: Verify the Gate MCP server source and keep the skill in read-only guidance mode until the MCP session and permissions are confirmed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-unified) <br>
- [Gate Skills Repository](https://github.com/gate/gate-skills) <br>
- [Gate Unified MCP Specification](references/mcp.md) <br>
- [Gate Unified Account Runtime Rules](references/gate-runtime-rules.md) <br>
- [Unified Account Scenarios](references/scenarios.md) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API Calls, configuration] <br>
**Output Format:** [Markdown reports, action drafts, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves API numeric strings exactly and requires explicit confirmation before write actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata; artifact frontmatter and changelog report 2026.4.3-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
