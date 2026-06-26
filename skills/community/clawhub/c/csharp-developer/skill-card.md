## Description: <br>
Use when building C# applications with .NET 8+, ASP.NET Core APIs, or Blazor web apps. Invoke for Entity Framework Core, minimal APIs, async patterns, CQRS with MediatR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhwa8685](https://clawhub.ai/user/lhwa8685) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, optimize, and test modern C# and .NET applications, including ASP.NET Core APIs, Blazor applications, Entity Framework Core data access, and performance-sensitive services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated authentication, authorization, and database migration examples may be unsafe if applied to real services without review. <br>
Mitigation: Review generated code before applying it, with particular attention to authentication flows, authorization policies, EF Core migrations, and production data access. <br>
Risk: Configuration examples may involve connection strings, JWT signing keys, or other secrets. <br>
Mitigation: Keep secrets in secure configuration such as environment variables, user-secrets, or a managed secrets store rather than hard-coding them in generated code or appsettings files. <br>


## Reference(s): <br>
- [Modern C# Patterns](references/modern-csharp.md) <br>
- [ASP.NET Core Patterns](references/aspnet-core.md) <br>
- [Entity Framework Core Patterns](references/entity-framework.md) <br>
- [Blazor Patterns](references/blazor.md) <br>
- [Performance Optimization](references/performance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with C# and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include domain models, DTOs, API endpoints, services, repository implementations, Program.cs and appsettings.json configuration, tests, and brief architectural rationale.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata; skill frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
