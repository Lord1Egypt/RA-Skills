## Description: <br>
Gate multi-account asset manager L2 skill for checking total assets, margin and liquidation risk, earnings snapshots, affiliate commissions, and confirmed unified-account actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect Gate account balances, margin and liquidation risk, earn and staking snapshots, affiliate commissions, and unified-account borrowing or collateral settings. Write operations are intended to be drafted, risk-disclosed, and executed only after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad authenticated financial-account data across account, asset, margin, earn, staking, affiliate, and rebate domains. <br>
Mitigation: Install only after review, prefer read-only Gate credentials unless write operations are required, and keep account snapshots confined to the authenticated user's context. <br>
Risk: The skill includes confirmed write authority for unified-account borrowing, collateral, leverage, and mode changes. <br>
Mitigation: Require a clear Action Draft with operation, target, amount or setting, rate where applicable, and risk note before accepting explicit single-use confirmation. <br>
Risk: The release depends on an external Gate runtime-rules document that is not pinned inside the reviewed package. <br>
Mitigation: Verify the referenced runtime-rules document before deployment and re-review the skill if those external rules change. <br>
Risk: Vague account prompts may reveal a broad financial snapshot. <br>
Mitigation: Scope ambiguous requests to the minimum relevant modules and disclose when broad account overview data will be queried. <br>


## Reference(s): <br>
- [Gate Exchange Account and Asset Manager on ClawHub](https://clawhub.ai/gate-exchange/gate-exchange-assets-manager) <br>
- [MCP execution specification](references/mcp.md) <br>
- [Behavior scenarios](references/scenarios.md) <br>
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, action drafts, MCP tool-call guidance, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read reports should include module tags and timestamps; write actions require an explicit Action Draft and single-use confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 2026.3.25-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
