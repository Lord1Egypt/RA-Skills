## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns combined alpha signal merging momentum, mean-reversion, and sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this paid signal endpoint to combine momentum, mean-reversion, and sentiment when evaluating crypto market conditions. Use its response as an input to analysis before making trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each authenticated request incurs a USDC charge, and repeated calls can accumulate costs.

Mitigation: Set a strict x402 maximum payment, check the current listed price, and use a wallet funded only for the intended request budget.

Risk: The example uses an EVM private key to authorize paid requests; exposing it could put the wallet at risk.

Mitigation: Keep EVM_PRIVATE_KEY in a protected secret store or environment, never include it in prompts or logs, and use a dedicated wallet with limited funds.

Risk: The returned market signal may be incomplete or unsuitable as the sole basis for a trade.

Mitigation: Check the response and corroborate it with independent information before acting, especially for high-stakes entries.

## Reference(s):

- [Combined Alpha endpoint](https://apexrunner.ai/signals/combined-alpha)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/combined-alpha)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [JSON signal response with a Python request example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid endpoint call returns a combined signal and component scores.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
