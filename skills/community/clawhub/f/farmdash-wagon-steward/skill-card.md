## Description: <br>
FarmDash Wagon Steward gives OpenClaw agents read-only DeFi portfolio analysis across EVM wallets, including balances, capital-efficiency signals, idle capital, position drift, and research-only rebalance proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect public EVM wallet portfolio state, identify idle or drifting positions, and generate research-only rebalance proposals without granting custody or execution authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FarmDash receives public wallet addresses for portfolio analysis and the optional API token if configured. <br>
Mitigation: Tell users what data is sent before use, avoid collecting private keys or seed phrases, and configure FARMDASH_API_KEY only when the user wants higher-tier access. <br>
Risk: The optional onboarding curl can link a public agent or wallet address to FarmDash analytics. <br>
Mitigation: Do not run onboarding automatically; require explicit, informed, manual consent before sending the request. <br>
Risk: Rebalance proposals may be stale or affected by liquidity, slippage, unpriced assets, or changing market conditions. <br>
Mitigation: Present proposals as research, time-bound the data, disclose missing or stale inputs, and require a separate execution skill with explicit confirmation for any transaction. <br>
Risk: Rate limits or unavailable chain data can make a portfolio snapshot incomplete. <br>
Mitigation: Surface unavailable chains or tokens, lower confidence for derived analysis, and avoid treating missing balances as zero. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-wagon-steward) <br>
- [FarmDash Agentic OS](https://www.farmdash.one/agents) <br>
- [FarmDash OpenAPI Schema](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash Wagon Steward Skill Source](https://www.farmdash.one/openclaw-skills/farmdash-wagon-steward/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown briefings with JSON portfolio snapshots and proposal objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only outputs include asOf, walletAddress, tier, staleAfterMs, and confidence when derived.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence; artifact frontmatter reports 0.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
