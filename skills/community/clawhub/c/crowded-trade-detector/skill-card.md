## Description: <br>
Detects when too many agents are in the same trade - liquidation risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to query a paid APEX Runner crypto-market signal before entering popular trades, avoiding liquidation-cascade exposure, or adding a crowding-risk gate to trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM private key and can authorize real USDC charges through x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet on Base mainnet and avoid exposing a primary wallet private key to the agent environment. <br>
Risk: Automatic paid requests may occur without clear per-call user confirmation. <br>
Mitigation: Require explicit price confirmation before each call and monitor repeated invocations. <br>


## Reference(s): <br>
- [Crowded Trade Detector signal](https://apexrunner.ai/signals/crowded-trade-detector) <br>
- [Crowded Trade Detector on ClawHub](https://clawhub.ai/kynto2001-ctrl/skills/crowded-trade-detector) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, analysis] <br>
**Output Format:** [JSON response containing crowded trade entries, crowding scores, severity, contrarian signals, market consensus, and timestamp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and can authorize paid x402 requests using USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
