## Description: <br>
Identifies optimal execution windows based on volatility and liquidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to time crypto order placement during volatile or latency-sensitive market conditions, using an x402-authenticated APEX Runner signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use a raw EVM wallet private key for automatically paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet, avoid exposing a primary wallet private key, and review the wallet environment before installation. <br>
Risk: Automatic calls can incur per-call charges. <br>
Mitigation: Track the stated per-call pricing and discounts, monitor call volume, and set operational limits before autonomous use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/execution-window-optimizer) <br>
- [APEX Runner execution window signal](https://apexrunner.ai/signals/execution-window-optimizer) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner slippage forecast signal](https://apexrunner.ai/signals/slippage-forecast) <br>
- [APEX Runner optimal order routing signal](https://apexrunner.ai/signals/optimal-order-routing) <br>
- [APEX Runner live ATR sizing signal](https://apexrunner.ai/signals/live-atr-sizing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown instructions with a Python request example and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and paid x402 requests from an EVM wallet with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
