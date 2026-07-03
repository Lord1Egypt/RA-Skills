## Description: <br>
Composite APEX score combining regime, momentum, and risk metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request a paid, real-time crypto trading composite signal for opportunity ranking and decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may authorize paid x402 requests without a clear confirmation step or spending limit. <br>
Mitigation: Use a dedicated wallet with limited USDC on Base, monitor call volume and costs, and disable the skill when paid requests are not intended. <br>
Risk: Use of an EVM private key can expose wallet funds if the execution environment or logs are compromised. <br>
Mitigation: Avoid primary wallets, scope funds to the minimum needed for calls, and keep EVM_PRIVATE_KEY out of shared logs and prompts. <br>


## Reference(s): <br>
- [Apex Composite Signal](https://apexrunner.ai/signals/apex-composite) <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/apex-composite) <br>
- [Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>
- [Combined Alpha Signal](https://apexrunner.ai/signals/combined-alpha) <br>
- [Signal Intelligence](https://apexrunner.ai/signals/signal-intelligence) <br>
- [Apex Alpha Score](https://apexrunner.ai/signals/apex-alpha-score) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown instructions with a Python example and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet with USDC on Base mainnet for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
