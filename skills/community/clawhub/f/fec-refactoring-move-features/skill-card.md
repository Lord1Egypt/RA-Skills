## Description:

Guides behavior-preserving frontend refactoring of feature ownership, statement placement, loops, and dead-code decisions across JavaScript, TypeScript, React, and Vue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers and agents use this skill to choose and apply small, verifiable moving-feature refactorings while preserving existing behavior and public contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moving public APIs or removing code could change observable behavior.

Mitigation: Review proposed diffs and affected callers, then verify behavior and public contracts after each small change.

## Reference(s):

- [Moving Feature Refactorings reference](references/moving-refactorings.md)
- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-refactoring-move-features)
- [Project homepage (package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with suggested code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One primary transformation at a time, with verification checkpoints.]

## Skill Version(s):

2.9.0 (source: package.json, metadata.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
