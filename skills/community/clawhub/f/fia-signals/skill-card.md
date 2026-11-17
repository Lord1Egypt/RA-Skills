## Description:

Fia Signals provides real-time crypto market intelligence, including market regime, sentiment, funding, price, liquidation, dominance, and technical signal data via the Fia Signals x402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odds7](https://clawhub.ai/user/odds7)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to request crypto market analysis such as market regime, fear and greed, funding rates, technical indicators, prices, dominance, and liquidation data. It is useful when an agent needs current market context before producing trading or market commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested crypto symbols and market-data actions to an external Fia Signals API.

Mitigation: Use the skill only when sharing the requested market-data scope with x402.fiasignals.com is acceptable.

Risk: Non-preview endpoints may require x402 payment despite artifact documentation that describes several endpoints as free preview.

Mitigation: Require an explicit spending gate before allowing an agent to invoke paid market-data calls.

Risk: Market signals and technical indicators can be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat results as market-data context rather than financial advice and require human review before trading decisions.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/odds7/skills/fia-signals)
- [Fia Signals API Gateway](https://x402.fiasignals.com)
- [Fia Signals x402 Discovery](https://x402.fiasignals.com/.well-known/x402.json)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Plain text summaries from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some endpoints may require x402 payment in USDC; preview output is available separately.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
