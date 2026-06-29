## Description: <br>
BTC dominance percentage with trend direction signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to retrieve BTC dominance, trend direction, and altcoin-season context for BTC versus altcoin allocation and capital rotation decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize x402 USDC payments for API calls. <br>
Mitigation: Use a dedicated low-balance wallet on Base containing only the USDC intended for this signal, and avoid reusing wallets that hold significant or unrelated assets. <br>


## Reference(s): <br>
- [APEX Runner BTC Dominance Signal](https://apexrunner.ai/signals/btc-dominance) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response from an x402-authenticated GET request, with concise usage guidance and example code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM wallet with USDC on Base mainnet for pay-per-call access.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
