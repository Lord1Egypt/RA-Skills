## Description: <br>
Supervised, policy-gated DeFi intelligence and execution manual for FarmDash MCP tools (60 tools). Covers swaps, simulations, perps, and autonomous operator features with MEV protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to research DeFi opportunities, compare routes, prepare signed swaps or perps, and run bounded automation through FarmDash tools while preserving user review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare wallet-affecting DeFi workflows, including swaps, perpetual contracts, and delegated automation. <br>
Mitigation: Use read-only mode unless the user is ready to verify every token address, chain, amount, fee, slippage, route, budget, allowlist, cooldown, and revocation setting before signing. <br>
Risk: Private keys, seed phrases, mnemonics, wallet exports, or OAuth tokens would create severe account and fund exposure if supplied to an agent. <br>
Mitigation: Do not provide private keys or seed phrases; rely on local wallet signing or explicitly configured bounded delegation. <br>
Risk: Onboarding, attribution analytics, referral routes, and bounded autopilot can introduce commercial or automated behavior. <br>
Mitigation: Treat these behaviors as opt-in and require explicit user approval before enabling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-signal-architect) <br>
- [FarmDash Agent Hub](https://www.farmdash.one/agents) <br>
- [FarmDash Skill Manual](https://www.farmdash.one/openclaw-skills/farmdash-signal-architect/SKILL.md) <br>
- [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash Fee Structure](https://www.farmdash.one/fees) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON examples, API procedure references, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare DeFi transaction workflows for local user signing or explicitly bounded delegation; read-only Scout access is available without an API key.] <br>

## Skill Version(s): <br>
1.2.19 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
