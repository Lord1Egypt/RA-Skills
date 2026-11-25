## Description:

Paid x402 endpoint: $0.014 USDC per call on Base. Returns contrarian setups when a liquidation cascade meets a crowded trade: fires only when Hyperliquid liquidation pressure is >80/100 and top wallets are crowded >70/100 on the side whose liquidations sit near price, with side, entry zone, target and invalidation (BTC, ETH, SOL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents can poll the endpoint for contrarian BTC, ETH, and SOL setups when liquidation pressure and wallet crowding meet the stated thresholds. Requests use x402 payment in USDC on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Four linked external pages were outside the security scan scope.

Mitigation: Review whether you trust each linked resource before following it.

Risk: The example probability estimate is heuristic and uncalibrated.

Mitigation: Treat probability labels as heuristic signal context and independently assess any proposed setup.

## Reference(s):

- [Capitulation Alert endpoint](https://apexrunner.ai/signals/capitulation-alert)
- [Crowded Trade Detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [Liquidation Pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [Check Trade Safety](https://apexrunner.ai/signals/check-trade-safety)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response containing alert status, setup side, entry zone, target, invalidation, and related signal fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The alert may be false; probability estimates are explicitly described as heuristic and uncalibrated.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
