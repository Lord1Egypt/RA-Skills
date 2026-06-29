## Description: <br>
Current arbitrage spread between Kraken and Hyperliquid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request a live Kraken versus Hyperliquid arbitrage spread signal before evaluating cross-exchange opportunities or sizing arbitrage legs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to let an agent spend from an EVM wallet for paid API calls. <br>
Mitigation: Use a dedicated low-balance wallet, configure spend caps and recipient allowlists before use, and avoid primary wallets or private keys with funds you cannot afford to lose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/arb-spread) <br>
- [Arb Spread signal endpoint](https://apexrunner.ai/signals/arb-spread) <br>
- [APEX Runner pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [Cross-exchange spread signal](https://apexrunner.ai/signals/cross-exchange-spread) <br>
- [Funding rate signal](https://apexrunner.ai/signals/funding-rate) <br>
- [Optimal order routing signal](https://apexrunner.ai/signals/optimal-order-routing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
