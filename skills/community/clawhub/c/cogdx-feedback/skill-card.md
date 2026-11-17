## Description:

CogDx Feedback helps agents submit post-change feedback to the Cerebratech CogDx API to check whether retraining, prompt changes, or instruction updates improved performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill after retraining, prompt changes, or instruction updates to submit feedback records and receive an improvement verification score, earned credits, and suggested next diagnostic steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feedback submissions can include prompts, responses, notes, identifiers, and evaluation data that may be sensitive.

Mitigation: Review and redact each payload before submission; use aggregate metrics or sanitized samples where possible.

Risk: The skill sends data to an external service and shared commons without clear retention, deletion, or consent terms in the artifact.

Mitigation: Confirm authorization and the provider's retention, deletion, and commons-sharing terms before production use.

## Reference(s):

- [CogDx Feedback API Reference](references/api.md)
- [CogDx Feedback endpoint](https://api.cerebratech.ai/feedback)
- [Cerebratech API catalog](https://api.cerebratech.ai/catalog)
- [ClawHub skill page](https://clawhub.ai/drkavner/skills/cogdx-feedback)
- [Publisher profile](https://clawhub.ai/user/drkavner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and inline HTTP command details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include request fields, response fields, error codes, and credit guidance for the feedback API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
