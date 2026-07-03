## Description: <br>
APEX proprietary alpha score for current market opportunity quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request a paid, real-time APEX Runner alpha score for ranking crypto market opportunity quality before trade entry or capital deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC through an EVM private key when requesting the paid signal. <br>
Mitigation: Use a dedicated low-balance wallet, review each request before it is made, and avoid exposing a primary wallet private key through EVM_PRIVATE_KEY. <br>
Risk: The signal is intended to inform crypto trading decisions before capital deployment. <br>
Mitigation: Apply independent trading limits and human review before using the signal to deploy significant capital. <br>


## Reference(s): <br>
- [ClawHub Apex Alpha Score Listing](https://clawhub.ai/kynto2001-ctrl/skills/apex-alpha-score) <br>
- [APEX Alpha Score Signal](https://apexrunner.ai/signals/apex-alpha-score) <br>
- [APEX Signal Pricing Tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [Combined Alpha Signal](https://apexrunner.ai/signals/combined-alpha) <br>
- [Agent Conviction Score Signal](https://apexrunner.ai/signals/agent-conviction-score) <br>
- [Institutional Apex Alpha Score Signal](https://apexrunner.ai/signals/apex-alpha-score-institutional) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and a funded EVM wallet with USDC on Base mainnet; x402 payment may be made per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
