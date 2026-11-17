## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns current arbitrage spread between Kraken and Hyperliquid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can query a paid Kraken-to-Hyperliquid spread signal to assess potential arbitrage opportunities and inform order sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The request signs a payment using an EVM private key and can spend USDC on Base.

Mitigation: Use a dedicated wallet with only the funds needed for calls, protect EVM_PRIVATE_KEY, and keep the configured payment cap at or below the intended amount.

Risk: The release changelog notes that the trading engines are paused, so a returned spread may not reflect a currently operating trading system.

Mitigation: Check signal freshness and validate prices independently before using it to make or execute a trade.

Risk: A spread signal does not account for all execution costs or guarantee that an arbitrage opportunity can be completed profitably.

Mitigation: Recalculate fees, slippage, liquidity, and transfer or settlement constraints before execution; treat the response as an input rather than an instruction to trade.

Risk: The clean security verdict covers the reported Markdown artifact and does not explain the skill's actual behavior.

Mitigation: Review the skill description and request behavior before installation and decide whether it fits the intended use.

## Reference(s):

- [APEX Runner arb-spread endpoint](https://apexrunner.ai/signals/arb-spread)
- [APEX Runner funding-rate signal](https://apexrunner.ai/signals/funding-rate)
- [APEX Runner optimal-order-routing signal](https://apexrunner.ai/signals/optimal-order-routing)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [JSON response with spread_pct, threshold_pct, and arb_viable fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid x402 request; the release describes an early-adopter rate of $0.007 USDC per call through 2027-01-01.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
