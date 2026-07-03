## Description: <br>
Cross-asset contagion risk score - detects systemic spillover risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to request a real-time cross-asset contagion score as a macro tail-risk overlay before leveraged positions or when monitoring spillover risk across equities and commodities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use an EVM private key for paid x402 requests. <br>
Mitigation: Use a dedicated low-balance Base wallet with only the USDC intended for calls, avoid reusing valuable wallet keys, and require explicit approval or a spending cap before calls. <br>
Risk: Each standard request may trigger a $25 on-chain payment. <br>
Mitigation: Review the pricing tier before use and cap or approve paid calls explicitly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/cross-asset-contagion) <br>
- [APEX Runner cross-asset contagion signal](https://apexrunner.ai/signals/cross-asset-contagion) <br>
- [APEX Runner pricing lookup](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner agent stress index signal](https://apexrunner.ai/signals/agent-stress-index) <br>
- [APEX Runner institutional cross-asset contagion signal](https://apexrunner.ai/signals/cross-asset-contagion-institutional) <br>
- [APEX Runner liquidation pressure signal](https://apexrunner.ai/signals/liquidation-pressure) <br>
- [Publisher profile](https://clawhub.ai/user/kynto2001-ctrl) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON response with contagion_risk, score, and trigger_assets fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet funded with USDC on Base for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
