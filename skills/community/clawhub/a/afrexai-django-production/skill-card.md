## Description:

Provides production Django engineering guidance for project architecture, ORM optimization, security hardening, testing, migrations, Celery, deployment, and operational readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review, structure, optimize, secure, test, and deploy Django applications for production. It can produce project health checks, implementation patterns, code examples, configuration guidance, and deployment checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The multi-tenant pattern could break tenant isolation if copied as written.

Mitigation: Require authenticated tenant membership checks, fail closed on missing or invalid tenant context, and review tenant filtering before production use.

Risk: Deployment, authentication, CI/CD, and data-access snippets may be applied without project-specific security review.

Mitigation: Treat generated snippets as templates, pin build tools where used, and require engineering review before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-django-production)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks, checklists, tables, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated deployment, authentication, CI/CD, and data-access changes require engineering review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
