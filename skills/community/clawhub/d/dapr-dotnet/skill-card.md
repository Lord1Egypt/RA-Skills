## Description:

Guides developers in building and adapting Dapr-enabled ASP.NET Core backends with layered architecture, reusable repositories and services, and consistent API responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weslon1987](https://clawhub.ai/user/weslon1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold or adapt .NET microservices with Dapr components, four-layer separation, database repositories, service patterns, and API health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API defaults may allow overly broad cross-origin access.

Mitigation: Restrict CORS origins to approved clients before deployment.

Risk: Raw SQL helpers can bypass repository safeguards or enable unsafe queries.

Mitigation: Limit raw SQL access to reviewed repository code and require parameterized queries.

Risk: Fixed zh-CN culture and local DEBUG sidecar startup may not fit every environment.

Mitigation: Make culture configurable and approve any DEBUG helper that starts daprd locally.

## Reference(s):

- [ClawHub release](https://clawhub.ai/weslon1987/skills/dapr-dotnet)
- [Project structure](references/project-structure.md)
- [Dapr API setup](references/dapr-api-setup.md)
- [Domain layer](references/domain-layer.md)
- [Infrastructure layer](references/infrastructure-layer.md)
- [Application and API results](references/result-application.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with C#, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Templates require adaptation and review before deployment.]

## Skill Version(s):

1.0.2 (source: server-resolved release; bundled skill frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
