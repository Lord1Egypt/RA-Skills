## Description: <br>
Analyze a specific Uniswap pool's performance, liquidity depth, fee APY, and risk factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DeFi analysts, and liquidity providers use this skill to evaluate a specific Uniswap pool before LPing or trading significant size. It summarizes pool identity, TVL, price, historical volume, fee APY, liquidity depth, concentration, and risk factors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates analysis to a pool-researcher subagent, so output quality depends on that subagent and the data it retrieves. <br>
Mitigation: Install only if you trust the publisher and the pool-researcher subagent your agent will call. <br>
Risk: Fee APY and LP suitability analysis are based on historical pool data and may not predict future returns. <br>
Mitigation: Treat fee APY and LP suitability output as informational financial analysis, not guaranteed returns. <br>
Risk: Pool, token, chain, or fee-tier ambiguity can produce missing or limited analysis. <br>
Mitigation: Provide explicit token contract addresses, chain, protocol version, and fee tier when available, and review any limited-data warning before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/analyze-pool) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>
- [README installation source](https://github.com/wpank/Agentic-Uniswap/tree/main/.ai/skills/analyze-pool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with structured pool metrics and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates pool research to a pool-researcher subagent and presents the returned analysis in a concise user-facing summary.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
