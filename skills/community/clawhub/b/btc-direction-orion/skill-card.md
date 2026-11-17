## Description:

Provides BTC UP/DOWN/NEUTRAL trading-bias snapshots with confidence bands using claimed RSI, Fear & Greed, and whale-flow signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokoju007](https://clawhub.ai/user/kokoju007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can request a quick BTC market-direction gate before swaps or execution, then optionally use Orion ACP for structured multi-timeframe signal data. Outputs should be treated as third-party trading signals requiring independent verification, not standalone financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence BTC trading decisions with unsupported or unaudited market-direction claims.

Mitigation: Require users to verify data sources, freshness, calculations, and market context independently before acting on any signal.

Risk: The skill promotes paid third-party signal offerings that may be mistaken for financial advice.

Mitigation: Present outputs as informational third-party signals, keep financial-risk disclosures visible, and avoid automated execution without separate review controls.

## Reference(s):

- [BTC Direction — Orion on ClawHub](https://clawhub.ai/kokoju007/skills/btc-direction-orion)
- [Orion ACP listing](https://app.virtuals.io/virtuals/1809)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text snapshot; structured JSON for paid signal offerings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include BTC bias, confidence band or score, timeframe, timestamp, and optional multi-timeframe market indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
