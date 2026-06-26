## Description: <br>
Supervised, policy-gated DeFi intelligence and execution manual for FarmDash MCP tools, covering swaps, simulations, perpetuals, and autonomous operator features with MEV protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi operators and agent developers use this skill to research on-chain opportunities, compare routes, simulate risk, and prepare user-authorized swaps, hedges, and bounded automation through FarmDash tools. It is intended for supervised workflows where wallet-changing actions require fresh quotes, simulations, explicit confirmation, or configured delegation limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real crypto trades, perpetual positions, and recurring automation. <br>
Mitigation: Use read-only mode by default; require fresh quotes, simulations, and explicit confirmation for every wallet-affecting action. <br>
Risk: Delegated or autopilot workflows could affect wallets without clear user opt-in if configured too broadly. <br>
Mitigation: Allow delegated operation only with explicit budgets, allowlists, cooldowns, risk bounds, and a documented revocation path. <br>
Risk: Airdrop, sybil, and timing guidance could be misused to influence anti-abuse systems. <br>
Mitigation: Use airdrop and sybil outputs only for risk review and educational planning, and avoid using jitter or automation to bypass protocol rules. <br>
Risk: Transactions are irreversible and may expose users to slippage, MEV, routing fees, gas costs, or incorrect destinations. <br>
Mitigation: Independently verify token contracts, chain IDs, destination addresses, fees, slippage, MEV risk, and simulation results before signing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-signal-architect) <br>
- [FarmDash Agent Hub](https://www.farmdash.one/agents) <br>
- [FarmDash Homepage](https://www.farmdash.one) <br>
- [FarmDash OpenAPI Specification](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash MCP Configuration](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash Fee Disclosure](https://www.farmdash.one/fees) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples, API call procedures, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference FarmDash MCP tools and OpenAPI endpoints; wallet-affecting actions require explicit user confirmation or bounded delegation.] <br>

## Skill Version(s): <br>
1.2.17 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
