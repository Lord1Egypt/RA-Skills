## Description:

Guides behavior-preserving frontend code restructuring through small, evidence-backed changes with verification and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to plan or perform small structural refactorings while preserving observable behavior. It directs them to establish a baseline, limit each change, verify results, and separate feature or migration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code edits could change observable behavior or affect more files than planned.

Mitigation: Review the proposed diff budget, check the baseline and step-by-step verification results, and require approval for broad or risky changes.

Risk: A regression may be hard to distinguish from an existing failure.

Mitigation: Record pre-existing failures before editing; revert a failing refactoring step and report any behavior preservation that remains unproven.

## Reference(s):

- [Refactoring principles](references/principles.md)
- [Refactoring workflow](references/workflow.md)
- [When to refactor](references/when-to-refactor.md)
- [Refactoring boundaries](references/refactoring-vs-feature-change.md)
- [Project homepage (listed in package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with a refactoring plan or implementation summary and, when executed, code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk classification, a diff budget, verification results, rollback details when applicable, and a PASS/PARTIAL/NOT PROVEN verdict.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
