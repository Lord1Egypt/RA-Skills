## Description:

Reviews consumer-visible API contracts for breaking changes and local design consistency across HTTP APIs, webhooks, event schemas, and similar surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API reviewers use this skill to evaluate API surface changes before release, focusing on backward compatibility, repo-local conventions, and durable contract design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect API specs, handlers, DTOs, sibling endpoints, and git history.

Mitigation: Run it only in repositories and files the user is authorized to review, and keep repository access scoped to the API contract under review.

Risk: A compatibility verdict can be wrong if the before-state or local precedent is incomplete.

Mitigation: Require findings to cite before/after contract evidence or in-repo precedent, and review migration recommendations before acting on them.

Risk: The review output may influence API design decisions even though the artifact does not automatically edit files.

Mitigation: Treat the report as guidance for human review, especially for breaking changes, versioning, deprecation windows, and consumer impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/api-contract-review)
- [Publisher profile](https://clawhub.ai/user/dennisrongo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with ranked breaking-change findings, design findings, and open questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should cite the before/after contract evidence or the in-repo precedent they rely on.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
