## Description:

Extract reusable UI/UX design systems from frontend codebases: design tokens, global styles, components, interaction patterns, and page templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsir0](https://clawhub.ai/user/xsir0)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to extract or create reusable frontend UI/UX specifications, including design tokens, component catalogs, page templates, accessibility notes, and migration plans while keeping business logic out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan broad areas of a frontend repository during UI source inventory.

Mitigation: Use it only on repositories where broad UI inspection is acceptable, and review scan scope before proceeding.

Risk: A refactor workflow may lead to UI-only code edits in the target repository.

Mitigation: Review and approve the proposed refactor plan before allowing changes, and keep edits scoped to UI/UX.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and optional file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a ui-ux-spec folder, design documentation, phased refactor plans, and UI-only code edits when the user selects a refactor workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
