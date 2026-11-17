## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns composite stress index measuring systemic risk across all APEX modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this paid endpoint to monitor systemic risk across APEX modules and consider it as one input to circuit-breaker decisions when stress rises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the request may authorize up to $0.01 even though the stated discounted charge is $0.007; it does not establish that the higher amount is charged.

Mitigation: Review the payment authorization cap and current price before each use, and set a cap you are willing to authorize.

## Reference(s):

- [Agent Stress Index endpoint](https://apexrunner.ai/signals/agent-stress-index)
- [Crowded Trade Detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [Portfolio Heat](https://apexrunner.ai/signals/portfolio-heat)
- [APEX Runner](https://apexrunner.ai)
- [ClawHub listing](https://clawhub.ai/kynto2001-ctrl/skills/agent-stress-index)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields include a stress score, stress level and trend, detected anomalies, monitored-agent count, and timestamp.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
