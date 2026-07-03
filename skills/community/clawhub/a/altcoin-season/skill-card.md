## Description: <br>
Altcoin season index - measures capital rotation from BTC to alts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request a paid x402 altcoin-season signal for sizing altcoin versus BTC exposure, timing rotation trades, and adding context alongside BTC dominance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize paid x402 API calls using a funded EVM private key. <br>
Mitigation: Use a dedicated wallet with very limited USDC, avoid primary wallet keys, set spending limits where possible, and require explicit confirmation before paid requests. <br>
Risk: Automatic payment authorization can create unintended spend if an agent calls the endpoint repeatedly. <br>
Mitigation: Gate calls behind user approval, monitor call history and pricing tiers, and cap wallet funding to the maximum acceptable loss. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/altcoin-season) <br>
- [Altcoin Season signal endpoint](https://apexrunner.ai/signals/altcoin-season) <br>
- [APEX Runner](https://apexrunner.ai) <br>
- [Pricing tier endpoint](https://apexrunner.ai/signals/my-pricing) <br>
- [BTC Dominance related signal](https://apexrunner.ai/signals/btc-dominance) <br>
- [Capital Rotation related signal](https://apexrunner.ai/signals/capital-rotation-signal) <br>
- [Regime related signal](https://apexrunner.ai/signals/regime) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with Python example code and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
