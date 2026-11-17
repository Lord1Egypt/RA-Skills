## Description:

Standardized backend REST API development following layered architecture patterns for building new REST APIs, implementing features, fixing bugs, and refactoring backend code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bayudsatriyo](https://clawhub.ai/user/bayudsatriyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, fix, or refactor Node.js and TypeScript REST APIs using a layered Express and Prisma architecture. It guides agents toward consistent route, controller, service, repository, DTO, mapper, validation, and error-handling patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-sensitive examples could lead agents to generate insecure user or list endpoints.

Mitigation: Review generated backend code before use, especially endpoints derived from the user-creation and list route patterns.

Risk: Public clients may be able to set roles or activation state if generated validation schemas follow the insecure example pattern.

Mitigation: Remove client-controlled role and activation-state fields from public create or update schemas, and enforce those values in trusted service logic.

Risk: Unbounded list queries can create performance and abuse risks.

Mitigation: Add bounded query validation for pagination, filtering, and limits before relying on generated route templates.

## Reference(s):

- [Error Handling Pattern](artifact/references/error-handling.md)
- [Senior Backend Engineer Mindset](artifact/references/senior-engineer-mindset.md)
- [Utilities & Helper Functions](artifact/references/utilities.md)
- [Input Validation Pattern](artifact/references/validation.md)
- [ClawHub Skill Page](https://clawhub.ai/bayudsatriyo/skills/backend-developer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes layered API module templates and backend implementation checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
