## Description: <br>
Computes Black-Scholes option prices, implied volatility, Greeks, and multi-leg strategy P&L for Chinese ETF, index, and commodity options using pure math. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as a calculation and reference aid for estimating option prices, implied volatility, Greeks, and strategy payoff scenarios in Chinese options markets. It is not an execution, trading, or margin-management system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Option prices, implied volatility, Greeks, and strategy P&L may be used as live trading decisions even though the evidence describes the skill as a calculation and reference aid. <br>
Mitigation: Treat outputs as estimates, verify market inputs independently, and require human review before trading or risk decisions. <br>
Risk: Black-Scholes assumptions can be inaccurate for American-style commodity options, dividend-sensitive ETF options, deep in-the-money contracts, margin requirements, and volatile markets. <br>
Mitigation: Use exchange rules, dividend adjustments, calibrated volatility surfaces, and specialized models where those factors materially affect the contract. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/china-options-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with tables, formulas, calculations, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure-math option-pricing guidance with no declared environment variables; python3 and curl are declared runtime binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
