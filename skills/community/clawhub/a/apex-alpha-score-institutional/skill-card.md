## Description: <br>
Institutional alpha score with full factor decomposition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and institutional trading teams use this skill to let agents request a paid x402-protected APEX Runner signal for alpha scoring, factor attribution, and pre-allocation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each x402-authenticated signal request can spend USDC. <br>
Mitigation: Require explicit confirmation before each call and use a dedicated low-balance wallet. <br>
Risk: The skill requires a raw EVM private key through EVM_PRIVATE_KEY. <br>
Mitigation: Never use a primary personal or treasury wallet; scope the key to a dedicated wallet intended only for this signal. <br>
Risk: The paid signal may influence allocation or trading analysis. <br>
Mitigation: Review returned signal data with internal risk controls before using it for large allocations. <br>


## Reference(s): <br>
- [Apex Alpha Score Institutional Signal](https://apexrunner.ai/signals/apex-alpha-score-institutional) <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/apex-alpha-score-institutional) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, API Calls] <br>
**Output Format:** [Markdown instructions with a Python example and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment authorization; requests can spend USDC.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
