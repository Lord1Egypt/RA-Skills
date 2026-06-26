## Description: <br>
CogDx provides cognitive diagnostics for AI agents, including calibration audits, bias detection, reasoning verification, consensus checks, and feedback-driven improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use CogDx to send selected agent predictions, outputs, reasoning traces, claims, and feedback to Cerebratech's diagnostics API for calibration audits, bias detection, reasoning review, deception checks, and consensus verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected prompts, outputs, reasoning traces, claims, context, and feedback to an external diagnostics service. <br>
Mitigation: Review and redact content before calls, and send only data approved for the external service. <br>
Risk: The skill uses a wallet-linked paid service and may spend credits or require payment. <br>
Mitigation: Use a dedicated wallet or account where possible, monitor credit usage, and require explicit approval before paid calls or feedback submission. <br>


## Reference(s): <br>
- [CogDx API](https://api.cerebratech.ai) <br>
- [CogDx ClawHub listing](https://clawhub.ai/drkavner/cogdx) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns diagnostic scores, findings, recommendations, model votes, credit status, and feedback receipts from the external API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
