## Description:

Verify documentation coverage and generate missing docs interactively.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit documentation coverage across Python, TypeScript/JavaScript, and Go projects, then review coverage gaps before choosing whether to generate missing documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation edits can introduce inaccurate or misleading project guidance.

Mitigation: Use --report-only for audit-only runs, review generated-file choices before allowing edits, and verify any accepted changes.

Risk: JavaScript lint verification can implicitly download packages when run through npx without local project dependencies.

Mitigation: Run lint verification through an existing project script or a project-local locked ESLint dependency.

## Reference(s):

- [Workflow reference](references/workflow.md)
- [Diataxis](https://diataxis.fr/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with JSON verifier results, inline shell commands, and optional code documentation edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in report-only mode to produce findings without applying documentation edits.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
