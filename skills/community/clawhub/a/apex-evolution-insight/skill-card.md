## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns weekly strategy evolution insights from APEX's self-improvement engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can request weekly strategy evolution insights to support performance reviews and long-term strategy calibration. Treat the response as informational and check its freshness before relying on it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Making a request authorizes an on-chain USDC payment using an EVM wallet and requires access to EVM_PRIVATE_KEY.

Mitigation: Keep the private key in a secrets manager, use a dedicated wallet with limited funds, and set a payment cap before making requests.

Risk: The release changelog says the engines are paused and removes claims of live trading data, while the artifact still describes the insights as computed from live market data.

Mitigation: Treat responses as informational and verify their source and freshness before using them to guide decisions.

## Reference(s):

- [APEX Evolution Insight endpoint](https://apexrunner.ai/signals/apex-evolution-insight)
- [APEX Signal Intelligence](https://apexrunner.ai/signals/signal-intelligence)
- [APEX Regime Transition](https://apexrunner.ai/signals/regime-transition)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response containing a week, strategy score, and top insight; usage instructions are provided in Markdown with a Python example.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly strategy insight; endpoint requests require payment in USDC on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
