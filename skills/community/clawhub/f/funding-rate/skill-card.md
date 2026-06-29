## Description: <br>
Funding rate analysis across perpetuals with arbitrage opportunity scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading analysts use this skill before opening perpetual futures positions, identifying funding arbitrage opportunities, and monitoring ongoing funding costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses wallet credentials for x402 payments and can spend funds. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit confirmation for each paid request and spending limit. <br>
Risk: Private key exposure could enable unauthorized wallet use. <br>
Mitigation: Keep wallet private keys out of chat and logs, and review the x402 facilitator and client package source before use. <br>


## Reference(s): <br>
- [Funding Rate Signal](https://apexrunner.ai/signals/funding-rate) <br>
- [Funding Rate Pricing](https://apexrunner.ai/signals/my-pricing) <br>
- [Related Signal: Funding Rate HL](https://apexrunner.ai/signals/funding-rate-hl) <br>
- [Related Signal: Arb Spread](https://apexrunner.ai/signals/arb-spread) <br>
- [Related Signal: OI Divergence](https://apexrunner.ai/signals/oi-divergence) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with Python example code and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment authorization; API responses include avg_rate_8h, arb_score, and recommended_action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
