## Description: <br>
Runs a paid Cerebratech CogDx calibration audit on an AI agent's sample outputs to compare stated confidence with actual correctness using statistical calibration metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to prepare calibration audit requests, interpret confidence-calibration metrics, and identify retraining targets before relying on agent uncertainty estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected agent prompts, responses, correctness labels, and confidence scores are sent to a paid external Cerebratech API. <br>
Mitigation: Remove secrets, personal data, proprietary prompts, and regulated data from samples before running an audit. <br>
Risk: The audit can deduct credits or require an x402 payment. <br>
Mitigation: Review and approve any x402 payment signature or credit deduction deliberately before submitting the request. <br>


## Reference(s): <br>
- [CogDx Calibration Audit API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/drkavner/cogdx-calibration) <br>
- [CogDx API Catalog](https://api.cerebratech.ai/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with HTTP examples and JSON request and response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe paid external API calls and required sample-output fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
