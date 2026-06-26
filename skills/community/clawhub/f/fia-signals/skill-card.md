## Description: <br>
Provides real-time crypto market data and technical analysis, including market regime, sentiment, funding rates, prices, dominance, liquidations, and technical signals via the Fia Signals x402 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Odds7](https://clawhub.ai/user/Odds7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to retrieve current crypto market intelligence for analysis workflows. It helps summarize market regime, sentiment, technical indicators, funding, prices, dominance, and liquidation data from the disclosed Fia Signals service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market queries and symbols are sent to the disclosed external Fia Signals API. <br>
Mitigation: Use the skill only when sharing those queries with x402.fiasignals.com is acceptable. <br>
Risk: Some endpoints can require x402 payment in USDC. <br>
Mitigation: Check endpoint pricing before use and prefer preview or free endpoints when evaluating the skill. <br>
Risk: Market signals may be incorrect, incomplete, delayed, or unsuitable for a user's trading objective. <br>
Mitigation: Treat outputs as market-data analysis rather than financial advice or a guarantee of trading outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Odds7/fia-signals) <br>
- [Fia Signals API gateway](https://x402.fiasignals.com) <br>
- [Fia Signals x402 discovery](https://x402.fiasignals.com/.well-known/x402.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text summaries; some endpoints may return JSON text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some endpoints require x402 payment in USDC; responses depend on the external Fia Signals service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
