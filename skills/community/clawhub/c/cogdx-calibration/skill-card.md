## Description:

Run a calibration audit on an AI agent's confidence estimates through the Cerebratech CogDx API using statistical metrics such as Brier scores and calibration curves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to submit labeled prompt/response samples and confidence scores to CogDx for calibration analysis before deployment or after noticing overconfidence or underconfidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt and response samples, correctness labels, and wallet or payment identifiers may be sent to Cerebratech/CogDx.

Mitigation: Get explicit user approval before balance checks or audit requests, and exclude customer data, secrets, proprietary prompts, regulated records, and sensitive model outputs unless provider privacy, retention, and payment terms are verified.

Risk: The audit is a paid third-party API call that may use x402 payment or credit balance.

Mitigation: Confirm the intended wallet or payment method, expected charge, and authorization before making a request.

Risk: Calibration conclusions depend on the quality and size of submitted labeled samples.

Mitigation: Use validated ground truth labels and the documented minimum of 10 samples, with 50 to 200 samples preferred for more reliable results.

## Reference(s):

- [CogDx Calibration Audit API Reference](references/api.md)
- [CogDx Calibration Audit endpoint](https://api.cerebratech.ai/calibration_audit)
- [CogDx API catalog](https://api.cerebratech.ai/catalog)
- [ClawHub skill page](https://clawhub.ai/drkavner/skills/cogdx-calibration)

## Skill Output:

**Output Type(s):** [API calls, Analysis, Guidance, JSON, Shell commands]

**Output Format:** [Markdown guidance with HTTP request examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a paid CogDx API call and sends calibration samples plus wallet or payment identifiers to a third-party service.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
