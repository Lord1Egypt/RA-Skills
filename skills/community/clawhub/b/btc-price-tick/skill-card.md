## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns real-time BTC price tick from live exchange feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this paid endpoint to retrieve a BTC price tick for low-latency price references, polling, or spread and momentum calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment authorization cap is $0.01 USDC per request, above the stated discounted price of $0.007.

Mitigation: Before use, confirm that authorizing up to $0.01 USDC per request is acceptable and set a payment cap appropriate to the intended spend.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/btc-price-tick)
- [BTC price tick endpoint](https://apexrunner.ai/signals/btc-price-tick)
- [Market tick](https://apexrunner.ai/signals/market-tick)
- [Apex Pulse](https://apexrunner.ai/signals/apex-pulse)
- [BTC dominance](https://apexrunner.ai/signals/btc-dominance)

## Skill Output:

**Output Type(s):** [API response, JSON data]

**Output Format:** [JSON BTC price tick with price fields and a timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid response per request.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
