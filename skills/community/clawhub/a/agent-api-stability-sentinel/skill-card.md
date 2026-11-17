## Description:

API compatibility and breaking-change detection specialist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nntrivi2001](https://clawhub.ai/user/nntrivi2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate API compatibility by comparing prior definitions, exercising modified endpoints, checking contracts and edge cases, and reporting breaking changes with migration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may drive live requests against production, third-party, financial, account, notification, or customer-data APIs.

Mitigation: Use only with explicit authorization, scoped hosts and methods, safe test credentials, synthetic or redacted payloads, conservative request limits, and separate approval for state-changing or destructive endpoints.

Risk: Live compatibility testing with real payloads can expose or modify sensitive data when used without clear boundaries.

Mitigation: Prefer isolated test environments and synthetic or redacted payloads; use production data only when the API owner has approved the test plan.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JSON compatibility report with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pass/fail/warning status, tested endpoint counts, breaking and non-breaking changes, version-bump recommendation, and migration steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
