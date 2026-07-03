## Description: <br>
Measures conviction strength of current APEX trade signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request a paid APEX Runner conviction score before trading, sizing positions, or comparing trade setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key for automatic paid x402 requests, which can spend wallet funds and expose wallet-linked usage metadata to the service. <br>
Mitigation: Use a dedicated low-balance wallet, avoid wallets holding important funds, and monitor or cap usage before allowing repeated invocations. <br>


## Reference(s): <br>
- [Agent Conviction Score service](https://apexrunner.ai/signals/agent-conviction-score) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/agent-conviction-score) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Guidance] <br>
**Output Format:** [JSON response from an x402-authenticated HTTPS GET request, with markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet with USDC on Base mainnet; each invocation can trigger a paid request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
