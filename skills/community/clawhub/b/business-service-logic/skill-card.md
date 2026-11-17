## Description:

Business module engineer skill for service-layer design, business logic extraction, and module-safe orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement or refactor service-layer business logic while keeping controllers thin, models persistence-focused, and module boundaries stable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced local Weline engineering standards may be unavailable or different in the target repository.

Mitigation: Review the referenced local standards before applying the skill and confirm which module, contracts, and validation path govern the work.

Risk: Service-layer refactors can unintentionally change controller, API, or model behavior.

Mitigation: Keep changes within the owning module, document any service contract assumptions, and run targeted unit tests plus an entry-point validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/business-service-logic)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with code changes, shell commands, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
