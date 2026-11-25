## Description:

Analyze pasted CORS response headers for dangerous combos — reflected origin with credentials, wildcard with credentials, null origin accepted, broad exposed headers. Offline, no probing. Use when the user pastes ACAO/ACAC headers or asks if a CORS setup is safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can review CORS response headers they provide and get concise findings about risky header combinations and suggested fixes. The lite check does not probe endpoints, and its findings should be verified in the endpoint's context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example curl command sends a live request, which conflicts with the stated offline-only scope.

Mitigation: Prefer analyzing headers supplied by the user or saved from an earlier request. Run the live-request example only when you intend to contact that service.

Risk: Exposed-header breadth is unchecked, and the security scan reports partial component coverage.

Mitigation: Treat results as a limited header-combination review, not a complete CORS assessment; verify exposed headers and endpoint behavior separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nenadzivotic/skills/cors-misconfig-check-lite)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON report with findings, severity, details, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes supplied response headers; does not test endpoint behavior or exposed-header breadth.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
