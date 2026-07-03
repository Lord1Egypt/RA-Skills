## Description: <br>
DCA entry signal with gate status, regime, and F&G conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to retrieve a paid DCA trading-signal API response before deciding whether DCA gate conditions are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent make paid requests using a wallet private key. <br>
Mitigation: Use a dedicated low-balance wallet and confirm expected price and call frequency before automated use. <br>
Risk: Trading-signal output may be treated as sufficient justification for DCA orders. <br>
Mitigation: Review signal responses and gate conditions before placing trades, especially in automated DCA workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/dca-signal) <br>
- [APEX Runner DCA Signal](https://apexrunner.ai/signals/dca-signal) <br>
- [APEX Runner Pricing Lookup](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402-authenticated request requiring EVM_PRIVATE_KEY and an EVM wallet funded with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
