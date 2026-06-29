## Description: <br>
Bollinger Band analysis with squeeze detection and breakout probability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request real-time Bollinger Band squeeze, band-position, and breakout-probability signals before breakout or mean-reversion trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize x402 payments. <br>
Mitigation: Use a dedicated low-balance wallet containing only the USDC intended for this skill, and do not reuse a wallet that holds significant funds or unrelated assets. <br>
Risk: The skill is pay-per-call, so automated agent loops can incur repeated USDC charges. <br>
Mitigation: Place explicit call limits or human approval around repeated requests, and monitor wallet balance and pricing tier changes. <br>
Risk: Trading signals may be incomplete or unsuitable for a specific trading decision. <br>
Mitigation: Treat the JSON response as one input to a broader review process rather than an instruction to trade. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/bb-analysis) <br>
- [APEX Runner bb-analysis signal](https://apexrunner.ai/signals/bb-analysis) <br>
- [APEX Runner pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner mean-reversion-scan signal](https://apexrunner.ai/signals/mean-reversion-scan) <br>
- [APEX Runner volume-analysis signal](https://apexrunner.ai/signals/volume-analysis) <br>
- [APEX Runner momentum-status signal](https://apexrunner.ai/signals/momentum-status) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Code, Configuration] <br>
**Output Format:** [JSON API response with Markdown usage guidance and Python example code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payments; the example response includes squeeze, position, and breakout_probability fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
