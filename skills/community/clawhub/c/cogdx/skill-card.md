## Description:

Cognitive diagnostics for AI agents. Calibration audits, bias detection, reasoning verification, and consensus building. Feedback builds shared reality across agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Cogdx to send selected agent outputs, claims, reasoning traces, confidence values, and feedback to Cerebratech's diagnostics API for calibration audits, bias scans, reasoning checks, deception audits, consensus verification, and feedback-based credit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected prompts, outputs, claims, context, confidence values, reasoning traces, feedback, and a wallet/account identifier to Cerebratech's external API.

Mitigation: Use it only with authorized data, redact secrets and private or regulated information, and avoid submitting proprietary reasoning unless disclosure is approved.

Risk: The diagnostics are produced by an external paid service and may influence agent decisions.

Mitigation: Review returned diagnostics before acting on them, and confirm payment, wallet, and rate-limit expectations before deployment.

## Reference(s):

- [Cogdx ClawHub skill page](https://clawhub.ai/drkavner/skills/cogdx)
- [drkavner ClawHub publisher profile](https://clawhub.ai/user/drkavner)
- [Cerebratech API](https://api.cerebratech.ai)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Python client methods, returned JSON-compatible dictionaries, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the requests Python package and a COGDX_WALLET value or wallet argument for API access.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
