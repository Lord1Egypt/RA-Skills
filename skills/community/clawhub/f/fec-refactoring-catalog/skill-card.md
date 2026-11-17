## Description:

Use when selecting or composing behavior-preserving refactoring techniques after structural evidence is known, especially when multiple candidate transformations, preconditions, or ordering choices must be compared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this catalog to select behavior-preserving refactorings from observed code structure and to order related transformations only when their preconditions fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A suggested transformation could change behavior or break public contracts.

Mitigation: Check preconditions and API, state, lifecycle, persistence, and rendering boundaries; verify each step before continuing.

Risk: Linked GitHub technique details may contain material beyond the packaged reference skill.

Mitigation: Review externally linked material separately before loading or following it.

## Reference(s):

- [Refactoring Catalog Index](references/catalog-index.md)
- [Refactoring Selection Guide](references/selection-guide.md)
- [Refactoring Composition Guide](references/composition-guide.md)
- [Frontend Craft project (listed homepage)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with refactoring technique IDs and conditional sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selection depends on observed causes, preconditions, and behavior-preservation checks.]

## Skill Version(s):

2.9.0 (source: ClawHub release, metadata.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
