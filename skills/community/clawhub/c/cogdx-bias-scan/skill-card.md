## Description:

Detects systematic inference-level biases in an AI agent's reasoning using the Cerebratech CogDx API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to submit selected prompt/response samples and feedback to Cerebratech for bias-pattern analysis before deployment or after recurring reasoning failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt/response samples and feedback are sent to a paid third-party API and may contain secrets, personal data, regulated data, system prompts, or unrelated history.

Mitigation: Review the exact records before scanning, remove secrets and personal or regulated data, avoid system prompts and unrelated history, and submit only samples intended for Cerebratech.

Risk: API usage can incur payment or consume credits.

Mitigation: Confirm the destination, cost, wallet or payment method, and credit balance before each scan.

Risk: Bias labels and retraining targets may be incomplete or unsuitable for high-stakes decisions without review.

Mitigation: Treat results as review inputs, validate recommendations with domain experts, and verify post-retraining behavior before deployment.

## Reference(s):

- [CogDx Bias Scan ClawHub Page](https://clawhub.ai/drkavner/skills/cogdx-bias-scan)
- [CogDx Bias Scan API Reference](references/api.md)
- [CogDx Detectable Bias Catalog](references/bias-catalog.md)
- [CogDx Bias Scan API Endpoint](https://api.cerebratech.ai/bias_scan)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples; the API response is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires selected prompt/response samples, optional failure feedback, and x402 payment or credits for the third-party API.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
