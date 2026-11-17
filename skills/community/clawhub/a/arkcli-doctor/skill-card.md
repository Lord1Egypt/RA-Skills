## Description:

Provides a unified Ark CLI entry point for diagnosing CLI health, accounts, errors, endpoints, models, metrics, reports, and media-origin features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Ark CLI diagnostic requests, interpret available CLI output, and find appropriate repair guidance. It also supports Ark media-origin feature checks for image and video URLs, with explicit cost disclosure and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media-origin verification sends the submitted media URLs to an external verification service.

Mitigation: Disclose the cost and external URL processing before starting verification, and wait for explicit user confirmation.

Risk: Suggested clock-repair commands may require elevated privileges.

Mitigation: Review the proposed command and its required permissions before running it.

Risk: Some local references could not be resolved during scanning, leaving parts of the guidance incompletely checked.

Mitigation: Review the referenced workflow documentation before relying on guidance in affected areas.

## Reference(s):

- [CLI health diagnostics](artifact/references/scope-cli.md)
- [Account diagnostics](artifact/references/scope-account.md)
- [Error code reference](artifact/references/error-codes.md)
- [Inference endpoint diagnostics](artifact/references/scope-infer-endpoint.md)
- [Model diagnostics](artifact/references/scope-model.md)
- [Metrics queries](artifact/references/scope-metrics.md)
- [Diagnostic reports](artifact/references/scope-report.md)
- [Media-origin verification](artifact/references/verify-origin.md)
- [Skill evaluation guidance](artifact/references/evals.md)
- [ClawHub release page](https://clawhub.ai/jasonstarlight/skills/arkcli-doctor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Concise Markdown with CLI commands; media-origin verification results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic conclusions are tied to available CLI output; media-origin results are passed through as server JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
