## Description:

Build secure access control with RBAC, ABAC, permissions, policies, and scope-based authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design and review authorization models, permission naming, policy evaluation, resource-level checks, and framework middleware for applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example authorization code may be incomplete for a production system's token contents, audit logging fields, or destructive actions.

Mitigation: Review and adapt the guidance before production use, especially around permission claims, audit logging, and delete endpoints.

Risk: Authorization examples can be misapplied if treated as drop-in production middleware.

Mitigation: Validate the resulting policy model and middleware against the application's resource model, role hierarchy, and server-side enforcement requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/authorization)
- [Skill homepage](https://clawic.com/skills/authorization)
- [Access control models](artifact/models.md)
- [Implementation patterns](artifact/patterns.md)
- [Framework middleware](artifact/middleware.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no automatic codebase access, persistence, data collection, or network behavior was found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
