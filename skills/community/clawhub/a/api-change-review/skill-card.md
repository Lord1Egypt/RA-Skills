## Description:

Review an API change for compatibility, validation, auth, error shape, idempotency, and observability, and classify it as additive, behavior-changing, or breaking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review API diffs or proposals, classify compatibility impact, identify risks around contracts, auth, errors, idempotency, and observability, and produce a minimal test and rollout plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Ritual Cloud upgrade can involve installing a third-party CLI and connecting workspace context to an external service.

Mitigation: Use the skill locally by default; only install or initialize the Ritual Cloud CLI intentionally after reviewing the package, version, permissions, and any workspace data or credentials it may access.

Risk: API change review output can be incomplete or misleading if the provided diff lacks affected callers, compatibility expectations, or rollout constraints.

Mitigation: Confirm contract surface, caller impact, compatibility assumptions, tests, and rollout notes against project evidence before applying recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ritual/skills/api-change-review)
- [Ritual homepage](https://ritual.work)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Code]

**Output Format:** [Markdown with structured review findings, compatibility verdicts, test plans, rollout notes, and optional code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first output based on provided code or content; optional Ritual Cloud setup guidance may be included when deeper workspace context is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
