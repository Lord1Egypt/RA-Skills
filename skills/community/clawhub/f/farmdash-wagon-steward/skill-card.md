## Description: <br>
Read-only DeFi portfolio aggregation skill for OpenClaw agents that returns wallet balances across EVM chains, scores capital efficiency, surfaces idle stablecoins, tracks position drift, and produces rebalancing proposals as research output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and DeFi agents use this skill to inspect public EVM wallet portfolio state, summarize balances and position health, and generate read-only research proposals for potential rebalancing or idle-capital review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public wallet addresses, selected chains, and any optional FarmDash bearer token to FarmDash for read-only portfolio analysis. <br>
Mitigation: Use only public wallet addresses you are comfortable sharing, review the optional token's purpose before configuring it, and avoid entering private keys, seed phrases, or mnemonics. <br>
Risk: The optional onboarding command registers a public agent or wallet address with FarmDash for tier checks and analytics. <br>
Mitigation: Run the onboarding curl only after explicit consent and only when you want FarmDash to associate that public address with the skill. <br>
Risk: Portfolio recommendations and rebalance plans may be stale or differ from live execution conditions. <br>
Mitigation: Treat outputs as research, verify current balances, liquidity, fees, and slippage before using a separate execution skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/farmdash-wagon-steward) <br>
- [FarmDash Agent Hub](https://www.farmdash.one/agents) <br>
- [FarmDash MCP Configuration](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash OpenAPI Spec](https://www.farmdash.one/agents/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON response examples and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only outputs include wallet snapshot timestamps, echoed wallet address, tier, stale-data hints, confidence where derived, and research-only recommendations.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence; artifact frontmatter version 0.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
