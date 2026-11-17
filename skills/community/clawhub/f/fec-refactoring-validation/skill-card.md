## Description:

Guides frontend developers through documenting behavior, selecting a safety net, validating refactoring steps, and reporting whether behavior preservation is proven.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to establish a pre-change behavior baseline, choose appropriate checks, and record whether a refactor preserved observable behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running project checks or reverting a refactoring step could affect the working tree.

Mitigation: Use a version-controlled development workspace and inspect changes before running checks or reverting a step.

Risk: Insufficient baseline or test coverage could make a behavior-preservation claim misleading.

Mitigation: Record coverage gaps and use PARTIAL or NOT PROVEN when available evidence cannot support PASS.

## Reference(s):

- [ClawHub release](https://clawhub.ai/bovinphang/skills/fec-refactoring-validation)
- [Behavior preservation](references/behavior-preservation.md)
- [Refactoring test checklist](references/refactoring-test-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavior-preservation record with baseline status, safety-net level, step checks, final validation, coverage gaps, and a PASS, PARTIAL, or NOT PROVEN verdict.]

## Skill Version(s):

2.9.0 (source: ClawHub release, metadata.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
