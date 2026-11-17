## Description:

A crypto trading decision agent for BTC, ETH, and SOL that applies layered market, liquidity, consensus, and risk checks to produce EXECUTE or NO TRADE decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericn26-star](https://clawhub.ai/user/ericn26-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can use this skill to structure informational crypto market analysis for BTC, ETH, and SOL. The skill turns supplied market context into a trade/no-trade proposal with risk gates and rejection reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be interpreted as financial advice or used directly for crypto trading decisions.

Mitigation: Treat outputs as informational trade ideas and require human review before any market action.

Risk: Actionable entry, stop, target, and expected-R fields could cause losses if connected to automated trading or account actions.

Mitigation: Do not connect this skill to exchange execution or account actions without a separate confirmation gate, risk disclosure, and stricter output schema.

Risk: Broad crypto and trading trigger terms may activate the skill during general market discussion.

Mitigation: Limit use to explicit requests for trade analysis with supplied market data and keep normal crypto discussion outside the execution workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericn26-star/skills/eric-minimax-crypto-trading)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text decision block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs EXECUTE_LONG, EXECUTE_SHORT, or NO TRADE with entry, stop, targets, expected R, and a structured reason when applicable.]

## Skill Version(s):

11.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
