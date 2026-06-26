## Description: <br>
Scans and compares USDC yield farming APYs on Base and Arbitrum, including vault performance, breakeven migration estimates, protocol risk notes, and APY history from DeFiLlama data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaoolucas](https://clawhub.ai/user/joaoolucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to research USDC yield opportunities, compare vaults, inspect APY history, and review protocol-level risk context before doing their own verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APY rankings and GO/MAYBE/NO-GO migration labels may be mistaken for financial advice or exact instructions to move funds. <br>
Mitigation: Treat outputs as research aids only; verify live APYs, pool IDs, smart-contract risk, bridge risk, withdrawal limits, slippage, tax impact, and actual gas or bridge costs before moving funds. <br>
Risk: Protocol risk, bridge behavior, low TVL, and simplified cost assumptions can make realized returns differ from estimates. <br>
Mitigation: Review protocol risk notes and current on-chain conditions independently, and use conservative assumptions when comparing vaults. <br>


## Reference(s): <br>
- [Protocol Reference](references/protocols.md) <br>
- [DeFiLlama Yields Pools API](https://yields.llama.fi/pools) <br>
- [DeFiLlama Yields Chart API](https://yields.llama.fi/chart/{pool_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style summaries with terminal tables and optional JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [APYs, pool rankings, and migration estimates are point-in-time research outputs and should be verified before financial action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
