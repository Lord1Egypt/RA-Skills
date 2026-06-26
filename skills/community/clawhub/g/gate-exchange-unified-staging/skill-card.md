## Description: <br>
Gate unified account operations skill for account equity, margin borrowing, repayment, leverage mode, collateral, and related limit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to query and manage Gate unified-account state, including equity, borrowable and transferable limits, loans, interest records, leverage settings, mode changes, and collateral configuration. It is intended for agent-assisted workflows backed by a configured local Gate MCP session and scoped Gate API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Gate unified-account mutations such as borrowing, repayment, mode changes, leverage changes, and collateral changes. <br>
Mitigation: Use API keys scoped to the documented Unified permissions, require an Action Draft, and execute only after immediate explicit user confirmation for the exact amount, target, and setting. <br>
Risk: A stale or changed confirmation could authorize an action different from the user's current intent. <br>
Mitigation: Treat confirmation as single-use, invalidate it when parameters or scope change, and require a fresh draft plus confirmation before each mutation. <br>
Risk: Rounding or normalizing returned balances, rates, leverage, or timestamps could mislead financial decisions. <br>
Mitigation: Preserve API numeric strings exactly as returned and include raw timestamps together with readable local times. <br>
Risk: Missing MCP configuration, authentication failures, or platform risk constraints can make write operations unsafe or impossible. <br>
Mitigation: Stop mutation attempts on setup, permission, or constraint failures and return read-only setup or remediation guidance instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-exchange-unified-staging) <br>
- [Gate skills repository homepage](https://github.com/gate/gate-skills) <br>
- [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate Unified MCP Specification](references/mcp.md) <br>
- [Gate Unified Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Unified Scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured action drafts, result summaries, exact API numeric strings, and MCP tool calls when configured] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GATE_API_KEY and GATE_API_SECRET through the local Gate MCP session; mutating actions require explicit single-use confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
