## Description: <br>
Composite stress index measuring systemic risk across all APEX modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request a paid APEX Runner signal for monitoring systemic risk across APEX modules, reducing exposure when stress rises, and informing circuit-breaker decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agent environment to access an EVM wallet private key for automatic paid calls. <br>
Mitigation: Use only a dedicated low-balance wallet and avoid exposing any primary wallet private key to the agent environment. <br>
Risk: Each x402-authenticated call can spend USDC on Base mainnet and the skill does not describe built-in spending controls. <br>
Mitigation: Confirm current costs before first use and apply external wallet, balance, or execution controls before allowing repeated calls. <br>


## Reference(s): <br>
- [Agent Stress Index endpoint](https://apexrunner.ai/signals/agent-stress-index) <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/agent-stress-index) <br>
- [Publisher profile](https://clawhub.ai/user/kynto2001-ctrl) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with Python example and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment authorization; endpoint responses include stress score, stress level, trend, anomalies, monitored agents, and timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
