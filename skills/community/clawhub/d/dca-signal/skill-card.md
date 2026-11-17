## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns DCA entry signal with gate status, regime, and F&G conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this paid endpoint at each DCA decision cycle to retrieve gate status and market-condition signals before considering an order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests use an EVM private key to authorize USDC payments on Base.

Mitigation: Use a dedicated wallet with limited funds and enforce a per-call spending cap.

## Reference(s):

- [DCA Signal endpoint](https://apexrunner.ai/signals/dca-signal)
- [Fear and Greed signal](https://apexrunner.ai/signals/fear-greed)
- [Portfolio Heat signal](https://apexrunner.ai/signals/portfolio-heat)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON signal response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid x402 request returns signal and gate-condition data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
