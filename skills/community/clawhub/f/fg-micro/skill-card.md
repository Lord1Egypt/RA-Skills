## Description: <br>
Lightweight Fear & Greed index snapshot for high-frequency polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to make paid x402-authenticated requests for a lightweight market sentiment signal before trade decisions or more expensive signal calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 requests can create repeated USDC charges during high-frequency polling. <br>
Mitigation: Use a dedicated low-balance Base wallet and set agent-side polling limits before enabling the skill. <br>
Risk: EVM_PRIVATE_KEY exposure would allow wallet misuse. <br>
Mitigation: Store the key only in a secret manager or protected environment variable, and avoid logging request configuration or environment values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/fg-micro) <br>
- [APEX Runner fg-micro signal](https://apexrunner.ai/signals/fg-micro) <br>
- [APEX Runner pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner](https://apexrunner.ai) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response with markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet with USDC on Base mainnet; each successful signal call may incur payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
