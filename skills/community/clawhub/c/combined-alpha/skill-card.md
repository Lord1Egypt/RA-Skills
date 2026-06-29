## Description: <br>
Combined alpha signal merging momentum, mean-reversion, and sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to request a paid real-time crypto alpha signal as a composite view, tie-breaker, or pre-entry check. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid calls can spend wallet funds if the skill is invoked repeatedly or automatically. <br>
Mitigation: Use a dedicated low-balance wallet, set explicit spend controls, and avoid automatic loops or high-frequency workflows. <br>
Risk: The skill requires an EVM private key for x402 payment authorization. <br>
Mitigation: Store the key as a secret, use a dedicated wallet rather than a primary wallet, and do not expose the key in prompts, logs, or shared files. <br>
Risk: The trading signal may influence high-stakes crypto decisions. <br>
Mitigation: Treat the signal as one input to a broader decision process and review outputs before acting on trades. <br>


## Reference(s): <br>
- [Combined Alpha signal endpoint](https://apexrunner.ai/signals/combined-alpha) <br>
- [Combined Alpha pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Composite related signal](https://apexrunner.ai/signals/apex-composite) <br>
- [Signal Intelligence related signal](https://apexrunner.ai/signals/signal-intelligence) <br>
- [Momentum Status related signal](https://apexrunner.ai/signals/momentum-status) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response from an x402-authenticated HTTPS GET request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and paid per-call access using an EVM wallet with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
