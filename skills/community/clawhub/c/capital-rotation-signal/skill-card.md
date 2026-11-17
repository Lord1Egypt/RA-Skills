## Description:

Calls a paid x402 endpoint that returns a signal about capital rotation among BTC, ETH, altcoins, and stablecoins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents can request a paid capital-rotation signal to inform analysis of BTC, ETH, altcoin, and stablecoin allocation. The skill documents the x402 wallet setup and the JSON response format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests use a wallet private key to authorize paid USDC calls, and returned allocation signals could be mistaken for trading advice.

Mitigation: Keep EVM_PRIVATE_KEY in a secure secret store, enforce a per-call spending cap, and independently assess signals before trading.

## Reference(s):

- [Capital Rotation Signal endpoint](https://apexrunner.ai/signals/capital-rotation-signal)
- [BTC Dominance signal](https://apexrunner.ai/signals/btc-dominance)
- [Altcoin Season signal](https://apexrunner.ai/signals/altcoin-season)
- [Regime Transition signal](https://apexrunner.ai/signals/regime-transition)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/capital-rotation-signal)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON signal response with x402 request guidance and a Python example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid signal response per call; the example configures a maximum USDC payment.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
