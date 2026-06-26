## Description: <br>
Detects systematic inference-level biases in an AI agent's reasoning via the Cerebratech CogDx API using statistical pattern matching against known cognitive bias signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to submit selected prompt and response samples for bias analysis, then review detected bias patterns, severity, retraining targets, and recommendations before deployment or after recurring failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompt and response samples are sent to Cerebratech for bias analysis. <br>
Mitigation: Submit only examples you are authorized to share, and remove secrets, personal data, and regulated data before scanning. <br>
Risk: The scan is a paid API call that may charge $0.10 or consume credits. <br>
Mitigation: Confirm the payment or credit cost before running a scan, and use a limited wallet or credit balance. <br>
Risk: Bias diagnoses and retraining recommendations may affect agent behavior in sensitive domains. <br>
Mitigation: Treat the results as review input, validate proposed retraining changes, and apply domain-specific oversight before deployment. <br>


## Reference(s): <br>
- [CogDx Bias Scan API Reference](references/api.md) <br>
- [CogDx Detectable Bias Catalog](references/bias-catalog.md) <br>
- [Cerebratech Bias Scan API](https://api.cerebratech.ai/bias_scan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples and shell-style HTTP request snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires selected prompt and response samples; minimum 10 outputs, recommended 30-100.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
