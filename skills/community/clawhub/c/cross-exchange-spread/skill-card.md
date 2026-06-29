## Description: <br>
Live spread between Kraken, Coinbase, and Hyperliquid for arb detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request live spread data across Kraken, Coinbase, and Hyperliquid before routing orders, detecting arbitrage windows, or feeding optimal-order-routing logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calls may spend USDC through wallet-based x402 billing. <br>
Mitigation: Use a dedicated low-balance Base wallet and set explicit spend limits before automated use. <br>
Risk: The EVM private key is required for authenticated requests. <br>
Mitigation: Store EVM_PRIVATE_KEY only in the agent environment and avoid logging, printing, or sharing it. <br>
Risk: Automated loops could create repeated paid calls. <br>
Mitigation: Avoid unbounded loops and add rate, budget, or call-count controls around agent workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/cross-exchange-spread) <br>
- [APEX Runner Cross Exchange Spread Signal](https://apexrunner.ai/signals/cross-exchange-spread) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls] <br>
**Output Format:** [Markdown instructions with a Python example and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and a Base mainnet wallet with USDC; each call may incur x402 payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
