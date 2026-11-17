## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns APEX service heartbeat — service status, BTC regime, Fear & Greed and BTC price in one cheap call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this paid endpoint to check APEX service status and current BTC market indicators before running health checks or relying on related signals. The response also reports a timestamp and validity window for freshness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an EVM wallet private key to authorize paid requests, and automated calls can spend USDC.

Mitigation: Keep EVM_PRIVATE_KEY in secret storage, preserve the maximum-payment policy shown in the example, and account for the per-call price before enabling repeated calls.

Risk: The response describes time-sensitive service and market conditions that may no longer be current when used.

Mitigation: Check the response timestamp and validity window before acting on the status or market indicators.

## Reference(s):

- [APEX Pulse endpoint](https://apexrunner.ai/signals/apex-pulse)
- [APEX Runner](https://apexrunner.ai)
- [Related APEX market-tick signal](https://apexrunner.ai/signals/market-tick)
- [Related APEX grid-health signal](https://apexrunner.ai/signals/grid-health)
- [Related APEX portfolio-heat signal](https://apexrunner.ai/signals/portfolio-heat)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [JSON service heartbeat with status, market indicators, timestamp, and validity window]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid x402 request per call; price and response freshness are time-sensitive.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
