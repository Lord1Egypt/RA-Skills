## Description: <br>
Full cross-asset contagion analysis with correlation matrices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and institutional risk teams use this skill to request live cross-asset contagion analysis, correlation matrices, and tail-risk indicators for systemic risk modelling and risk committee reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid x402 requests from the configured wallet. <br>
Mitigation: Install only when paid calls are intended, use a dedicated wallet with minimal funds, and configure spend caps or recipient allowlists where available. <br>
Risk: Automated use can accumulate costs per request. <br>
Mitigation: Review the displayed per-call pricing and wallet call history before allowing automated requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/cross-asset-contagion-institutional) <br>
- [APEX Runner signal endpoint](https://apexrunner.ai/signals/cross-asset-contagion-institutional) <br>
- [APEX Runner pricing status](https://apexrunner.ai/signals/my-pricing) <br>
- [Related signal: cross-asset-contagion](https://apexrunner.ai/signals/cross-asset-contagion) <br>
- [Related signal: regime-confluence-institutional](https://apexrunner.ai/signals/regime-confluence-institutional) <br>
- [Related signal: apex-alpha-score-institutional](https://apexrunner.ai/signals/apex-alpha-score-institutional) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis] <br>
**Output Format:** [JSON response containing contagion score, correlation matrix, and tail-risk fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
