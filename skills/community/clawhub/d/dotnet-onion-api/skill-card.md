## Description:

Scaffold a new .NET solution with Web API and Worker microservices using Onion architecture, EF Core, and layered .NET patterns while avoiding common legacy anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold new .NET Onion-architecture APIs, add end-to-end feature slices, and add BackgroundService worker microservices with build and test verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API authentication templates may include placeholder JWT secrets or incomplete token validation.

Mitigation: Reject placeholder JWT secrets at startup, load secrets from a secret manager or environment, and require issuer, audience, and lifetime validation before production use.

Risk: Generated error handling may expose stack traces in staging responses.

Mitigation: Remove stack traces from staging and production responses before relying on the generated API.

Risk: The skill can scaffold a new solution and write many files.

Mitigation: Confirm the intended target directory and scaffolding mode before allowing file creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/dotnet-onion-api)
- [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
- [NuGet flat container API](https://api.nuget.org/v3-flatcontainer/<package-id-lowercase>/index.json)
- [anti-patterns.md](references/anti-patterns.md)
- [solution-layout.md](references/solution-layout.md)
- [appsettings.md](references/templates/appsettings.md)
- [base-controller.cs.md](references/templates/base-controller.cs.md)
- [csproj-files.md](references/templates/csproj-files.md)
- [dbcontext.cs.md](references/templates/dbcontext.cs.md)
- [exception-middleware.cs.md](references/templates/exception-middleware.cs.md)
- [feature-slice.md](references/templates/feature-slice.md)
- [program-cs.md](references/templates/program-cs.md)
- [worker-program.cs.md](references/templates/worker-program.cs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write many scaffolded .NET source and configuration files after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
