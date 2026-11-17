## Description:

Use this skill when a backend engineer, platform engineer, or API team needs a structured review of a REST/HTTP API design before clients build against it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review draft REST/HTTP APIs from an OpenAPI spec, design document, or endpoint sketch. It helps API authors find design issues across resource modeling, HTTP semantics, data shapes, errors, pagination, idempotency, versioning, auth, and rate limits before clients depend on the API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided API specs or design documents may contain live secrets, customer identifiers, partner credentials, or other sensitive pre-release details.

Mitigation: Redact sensitive values before using the skill, and rotate any live secrets that were pasted into the review artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/api-design-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured as an API design review report with severity-tagged findings, a Top-5 must-fix list, a ship verdict, a required-before-ship checklist, and open questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API spec, design document, or endpoint sketch plus review context such as consumers, lifecycle stage, constraints, and authentication scheme.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
