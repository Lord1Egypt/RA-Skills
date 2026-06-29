## Description: <br>
Detects capital rotation between BTC, ETH, alts, and stables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to call an x402-authenticated APEX Runner endpoint for real-time crypto capital rotation signals across BTC, ETH, alts, and stables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM wallet private key to authorize USDC payments for each API call. <br>
Mitigation: Use a dedicated wallet funded only with USDC you are willing to spend, monitor repeated calls, and avoid wallets holding significant or unrelated assets. <br>


## Reference(s): <br>
- [Capital Rotation Signal](https://apexrunner.ai/signals/capital-rotation-signal) <br>
- [Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>
- [BTC Dominance Signal](https://apexrunner.ai/signals/btc-dominance) <br>
- [Altcoin Season Signal](https://apexrunner.ai/signals/altcoin-season) <br>
- [Regime Transition Signal](https://apexrunner.ai/signals/regime-transition) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response data with concise agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM private key for x402 payment authorization and returns paid real-time trading signal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
