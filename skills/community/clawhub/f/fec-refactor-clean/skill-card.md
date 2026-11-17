## Description:

Helps developers identify and remove proven-unused frontend code, styles, routes, and dependencies without changing user-visible behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to identify and remove demonstrably unused code in small, verified batches, while leaving uncertain or behavior-changing changes for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting code that is reached through dynamic references, routes, configuration, shared components, styles, or public APIs can break behavior.

Mitigation: Require evidence of non-use, review proposed deletions, leave uncertain items for manual confirmation, and run affected lint, type-check, test, and build checks before accepting changes.

## Reference(s):

- [Refactor Clean release](https://clawhub.ai/bovinphang/skills/fec-refactor-clean)
- [Cleanup report template](artifact/references/report-template.md)
- [Project homepage (package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Code changes and Markdown cleanup reports with verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports identify cleanup evidence, skipped items, verification steps, and residual risks.]

## Skill Version(s):

2.9.0 (source: release metadata, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
