---
name: dotnet-onion-api
description: Scaffold a new .NET solution (Web API + Worker microservices) using ONION architecture and EF Core, codifying battle-tested layered patterns and explicitly avoiding the common pitfalls of legacy stored-procedure-centric codebases. Use this skill whenever the user asks to "create a new dotnet project", "scaffold a .NET API", "new C# solution", "add a worker microservice", "add a feature end-to-end", or mentions "ONION", "Clean Architecture", "Onion Architecture", or "the layered .NET patterns I like". Three modes — (1) full solution scaffold, (2) add a feature slice through all layers, (3) add a BackgroundService worker microservice.
---

# .NET ONION API Scaffolder

Generate a production-grade .NET solution that keeps the **good** layered patterns (Api → Application → Infrastructure → Domain separation, base classes for cross-cutting concerns, extension-method wiring in `Program.cs`, JWT, AutoMapper, auto-DI, unified error responses) and eliminates the **bad** ones often seen in legacy .NET codebases (stored-procedure-centric reflection repositories, EF6 on netstandard2.1, polling console-app workers, swallowed exceptions, mutable per-request state on base service classes, mixed ADO/Dapper/EF6 data access, missing `CancellationToken` plumbing).

## When to use this skill

Trigger on any of:

- "create a new dotnet project / .NET solution / C# project"
- "scaffold a .NET Web API"
- "new microservice in .NET" / "add a worker service"
- "use the patterns I like" / "use my layered .NET conventions" (in a .NET context)
- "ONION architecture" / "Clean Architecture" / "layered .NET project"
- "add a feature end-to-end" / "add a slice" (API + service + repository + EF entity + tests)
- The user pastes a feature spec and asks you to wire it through the layers of a .NET solution

If unsure whether the user wants a brand-new solution vs. an addition to an existing one, ask once — don't guess.

## Three operating modes

Pick the mode from the user's request. If ambiguous, ask.

| Mode | Trigger | Output |
|------|---------|--------|
| **`scaffold-solution`** | "new project", "scaffold solution", empty directory | Full ONION solution: Domain, Application, Infrastructure, Api, Workers (optional), Tests. |
| **`add-feature`** | "add `<Entity>` end-to-end", "wire up `<feature>` through all layers" | Entity + EF config + repository (port + adapter) + use-case service + DTO + controller + AutoMapper profile + unit test. |
| **`add-worker`** | "new worker", "add microservice for queue X" | New `Workers.<Name>` project (BackgroundService) referencing Application + Infrastructure, with queue/service-bus consumer and graceful shutdown. |

## Workflow

### Step 1 — Determine the target framework (don't hard-code)

Never bake a hard-coded `<TargetFramework>` into generated projects — resolve it at scaffold time. Before generating `.csproj` files:

1. Check the user's environment first: run `dotnet --list-sdks` to see installed SDKs.
2. If a current LTS SDK is installed, prefer the highest installed LTS (`net8.0`, `net10.0`, etc.).
3. If unsure which is the current LTS, fetch the latest .NET support policy via context7 (`mcp__plugin_context7_context7__resolve-library-id` → `query-docs` for ".NET release schedule" / "dotnet support policy") or WebFetch `https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core`. Quote the version you picked back to the user before generating.
4. Pin EF Core, ASP.NET Core, and `Microsoft.Extensions.*` package versions to the **latest stable for that TFM** — look them up via context7 (`Microsoft.EntityFrameworkCore`, `Microsoft.AspNetCore.Authentication.JwtBearer`, etc.) rather than guessing. Never hand-paste a version you don't have a source for.
5. State the chosen TFM and package versions in your reply before writing files, so the user can object before scaffolding.
6. Concrete resolution commands when context7 is unavailable: `dotnet package search <PackageId> --take 1` or WebFetch `https://api.nuget.org/v3-flatcontainer/<package-id-lowercase>/index.json` (last non-preview entry = latest stable). Never write a version string you did not just resolve this session — no versions from memory, no wildcards, no invented numbers.

**API-drift guard.** The version you resolved in this step decides the API shape — training-data memory is the least trustworthy source in this workflow. Highest-risk hallucination zones:

- EF Core APIs across majors (e.g. `HasCheckConstraint` moved into `ToTable(t => t.HasCheckConstraint(...))` in EF7; query/interceptor APIs get renamed between majors).
- Hosted-service and `Host` builder idioms — `Host.CreateApplicationBuilder` (post-.NET 7) vs the older `CreateDefaultBuilder` callback style; don't mix the two.
- TFM defaults: newer TFMs flip `<Nullable>` / `<ImplicitUsings>` behavior — templates must match the resolved TFM, not a remembered one.
- OpenAPI/Swagger: .NET 9+ templates dropped Swashbuckle for built-in `Microsoft.AspNetCore.OpenApi` (`AddOpenApi()` / `MapOpenApi()`). Pick the approach matching the resolved TFM; never wire both.
- Test stack majors: xunit v3 ships as the `xunit.v3` package with different runner wiring than `xunit` 2.x; AutoMapper 13+ self-registers (no `.Extensions.Microsoft.DependencyInjection` package). Match templates to what you resolved, not to package names from memory.

If you are not certain a symbol exists in the resolved version, verify it (context7 docs lookup, or read the restored package surface under `~/.nuget/packages/`) **before** writing code that depends on it.

### Step 2 — Gather inputs (ask once, in one batch)

For `scaffold-solution`, use `AskUserQuestion` to collect:

- **Solution name** (e.g. `Acme.Billing`). Used for namespace root and `.sln`.
- **First feature/entity** (optional, e.g. `Customer`) — if provided, also run `add-feature` for it after scaffold.
- **Auth**: JWT bearer with HS256 (symmetric) **or** JWT with asymmetric (RS256/JWKS) **or** none-yet.
- **Include any Workers now?** If yes, ask for their names (comma-separated, e.g. `EmailSender, PdfPrinter`).
- **Optional extras**: Serilog + OpenTelemetry? Dockerfile? GitHub Actions CI? Testcontainers integration tests? (Default: skip — only add if asked.)

For `add-feature`: entity name, properties (name + C# type + nullability), whether it needs CRUD controller or only specific endpoints.

For `add-worker`: worker name, trigger source (Azure Storage Queue / Service Bus / Timer), message DTO type (if known).

### Step 3 — Generate files

Use the **templates in `references/templates/`** as the source of truth for file contents. Apply these rules:

- Use `Write` for new files. Never use `Edit` on files you're creating fresh.
- Replace all `{{Solution}}`, `{{Feature}}`, `{{Worker}}` placeholders consistently.
- Create directories before files. On Windows shell use PowerShell `New-Item -ItemType Directory -Force`.
- After scaffolding, run `dotnet sln add` for every project and `dotnet build` to verify the solution compiles. Report build output to the user.
- Do **not** run `dotnet new` to create the projects — write the `.csproj` and `.cs` files directly from templates so the layout matches exactly.
- If a `dotnet new` template IS run anyway (user's insistence): **the SDK wins on formats it owns** (`.sln` contents, `obj/`/`bin/` artifacts), **this skill wins on everything else** — overwrite template boilerplate with the skill's templates, keep this skill's project split and folder names. Reconcile deliberately and list every deviation in your report; never silently abandon the skill's patterns, never fight the SDK on formats it owns.

### Step 4 — Verify and report

- Run `dotnet build` from the solution root. If it fails, fix the **first** error (later errors are usually cascade) and rebuild — never leave a broken scaffold.
- Run `dotnet test` if any test project exists.
- Do **not** run `dotnet ef migrations add` or `dotnet ef database update` yourself unless the user confirmed a reachable database — report the migration command as a next step instead. The delivery bar is the build gate, not the migration.
- Known failure signature: `NETSDK1045` ("The current .NET SDK does not support targeting …") means the TFM you picked outruns the installed SDK — re-run `dotnet --list-sdks` and re-pin to the highest installed LTS; do not install a new SDK unprompted.
- **A scaffold that hasn't compiled is not delivered.** Paste the actual proof lines in your report (`Build succeeded.` / `0 Error(s)`, and the `Passed! - Failed: 0` test summary). Never report success from memory of the steps you intended, and never report partial success as success — if something is red, say exactly what is red.
- **CLI failure protocol** (applies to `dotnet new`, `dotnet sln add`, `dotnet build`, `dotnet test`): read the full error output, change exactly one thing, retry once. If the same step fails twice, stop scaffolding and surface the verbatim error to the user — do not keep generating files on top of a broken base, and do not re-run the identical command hoping for a different result.
- Reply with a short summary: solution path, projects created, TFM chosen, package versions, next steps (e.g. "run `dotnet ef migrations add Initial -p src/{{Solution}}.Infrastructure -s src/{{Solution}}.Api`").

## Solution layout (canonical)

See [`references/solution-layout.md`](references/solution-layout.md) for the full tree and dependency rules.

```
{{Solution}}/
  {{Solution}}.sln
  src/
    {{Solution}}.Domain          # entities, value objects, domain events. NO project refs.
    {{Solution}}.Application     # use-case services + ports (interfaces) + DTOs + validators. refs Domain.
    {{Solution}}.Infrastructure  # EF Core DbContext, repository adapters, external clients (Azure, email, auth). refs Application+Domain.
    {{Solution}}.Api             # Controllers, Middleware, Filters, Program.cs. refs Application+Infrastructure.
    {{Solution}}.Workers.<Name>  # BackgroundService microservices. refs Application+Infrastructure.
    {{Solution}}.Contracts       # (optional) public DTOs / API contracts shared with clients.
  tests/
    {{Solution}}.UnitTests       # xUnit + NSubstitute. Tests Application use-cases with mocked ports.
    {{Solution}}.IntegrationTests# WebApplicationFactory + Testcontainers (SQL Server). Real DB + real pipeline.
```

**Dependency rule (enforced):** outer → inner only. Domain has zero project references. Application references Domain only. Infrastructure may reference both. Api/Workers reference Application + Infrastructure but never each other.

## Required code patterns

Use these exact patterns when generating files. Full templates are in `references/templates/`.

### Keep

- **`BaseController`** with `[ApiController]`, `[Route("api/[controller]")]`, `[Authorize]`, injected `IUserContext` — see [`references/templates/base-controller.cs.md`](references/templates/base-controller.cs.md).
- **Base use-case service** with constructor-injected `IUserContext` (no public mutable user property — a common bug in legacy bases).
- **Thin `Program.cs`** that calls only extension methods (`AddApplication`, `AddInfrastructure`, `AddApiServices`, `AddJwtAuth`, `AddSwaggerDocs`, `AddCorsPolicies`). See [`references/templates/program-cs.md`](references/templates/program-cs.md).
- **Auto-registration** via `Scrutor` for ports → adapters (replaces `NetCore.AutoRegisterDi`, modern + maintained). Singletons/options registered explicitly.
- **Strongly-typed `AppSettings` + `ConnectionStrings`** bound via `IOptions<T>` (don't register the raw POCO as singleton — use `services.Configure<T>(...)` and inject `IOptions<T>`).
- **AutoMapper** with assembly scan: `services.AddAutoMapper(typeof(ApplicationAssemblyMarker).Assembly)`.
- **Centralized exception middleware** with env-aware response — see [`references/templates/exception-middleware.cs.md`](references/templates/exception-middleware.cs.md).
- **Unified validation error response** via `InvalidModelStateResponseFactory`.
- **JWT auth wiring** in a `RegisterAuth` extension method.
- **Minimal comments in generated code.** Default to no comments. Only add one when the *why* is non-obvious — a workaround for a specific framework bug (with a link), a subtle invariant the code depends on, a domain rule that isn't visible from the names. Never write XML doc-comment blocks (`/// <summary>...`) on internal members; reserve them for genuinely public API surface that ships to consumers. Never restate *what* the next line does, never leave `// TODO` without an issue link. One short line max — no multi-line comment blocks. Well-named identifiers carry the *what*; comments earn their place only when they carry *why*.

### Eliminate (anti-patterns)

Every one of these is forbidden in generated code. See [`references/anti-patterns.md`](references/anti-patterns.md) for the rationale of each.

- ❌ Stored-procedure-first data access. **Use EF Core with LINQ**; only drop to raw SQL via `FromSqlInterpolated`/`ExecuteSqlInterpolated` for legitimate perf/legacy reasons, and never with reflection-based parameter mapping.
- ❌ `dynamic` / `ExpandoObject` for query parameters.
- ❌ Reflection-based `DataRow → object` mappers. EF Core handles this.
- ❌ EF6 + `netstandard2.1`. Use **EF Core (latest)** on the chosen TFM.
- ❌ Empty `catch {}` blocks. Either handle the exception meaningfully or let it propagate to the middleware.
- ❌ Mutable `public User { get; set; }` on a service base class — request-scoped state belongs in the scoped `IUserContext` only.
- ❌ Polling `while (true) { Task.Delay(5s) }` console-app workers. Use `BackgroundService` with `CancellationToken stoppingToken` and SDK-native receive loops — see [`references/templates/worker-program.cs.md`](references/templates/worker-program.cs.md).
- ❌ Booting hosted services with `serviceProvider.GetService<T>()` in `Program.cs`. Register them via `services.AddHostedService<T>()`.
- ❌ Auto-registering everything as `Scoped` indiscriminately. Use Scrutor's lifetime selectors, and register Azure SDK clients / `IHttpClientFactory` clients / options as singletons explicitly.
- ❌ Newtonsoft.Json + `DefaultContractResolver` (PascalCase). Use **System.Text.Json** with `JsonNamingPolicy.CamelCase` by default. Add Newtonsoft only if a specific dependency demands it.
- ❌ Missing `CancellationToken` parameters. Every async public method takes `CancellationToken ct` as the **last** parameter and forwards it.
- ❌ Per-tenant repositories under `Repositories/{TenantName}/`. Multi-tenant behavior goes through a strategy injected via DI, not folder forks.
- ❌ Hard-coded multi-tenant magic fallbacks (e.g. defaulting `ClientId` to a literal string when claims are missing). Multi-tenancy comes from `IUserContext` or fails fast.
- ❌ Commented-out dead code in generated files.
- ❌ Controllers that bypass `BaseController` (consistency is mandatory; if a public endpoint needs `[AllowAnonymous]`, declare it on the action).

## Operating-mode playbooks

### Mode 1 — `scaffold-solution`

1. Pick TFM and package versions per **Step 1**. Quote them.
2. Ask the inputs per **Step 2**. Wait for answers.
3. Generate, in this order:
   1. `.sln` file (use `dotnet new sln -n {{Solution}}` *only* to produce the sln; everything else is hand-written from templates).
   2. `src/{{Solution}}.Domain/` (csproj + `DomainAssemblyMarker.cs` + sample `Entity` base if relevant).
   3. `src/{{Solution}}.Application/` (csproj + assembly marker + `Common/` with `IUserContext`, `Result<T>` if requested, `IUnitOfWork` port, `IRepository<T>` port).
   4. `src/{{Solution}}.Infrastructure/` (csproj + `Persistence/AppDbContext.cs` + `Persistence/EntityConfigurations/` folder + `Persistence/UnitOfWork.cs` + `Auth/UserContext.cs` + `DependencyInjection.cs` with `AddInfrastructure`).
   5. `src/{{Solution}}.Api/` (csproj + `Program.cs` + `Extensions/` folder + `Middlewares/ExceptionHandlerMiddleware.cs` + `Controllers/BaseController.cs` + `appsettings.json`/`appsettings.Development.json`).

      **Checkpoint:** `dotnet sln add` items 1–5 and `dotnet build` now, before generating workers and tests — a failure here localizes to the core projects; a failure after the full tree does not. Apply the Step-4 failure protocol at this checkpoint too.

   6. `src/{{Solution}}.Workers.<Name>/` per worker requested.
   7. `tests/{{Solution}}.UnitTests/` (csproj + xUnit + NSubstitute + AutoFixture).
   8. `tests/{{Solution}}.IntegrationTests/` (csproj + `Microsoft.AspNetCore.Mvc.Testing` + `Testcontainers.MsSql`) — only if user asked for it.
4. `dotnet sln {{Solution}}.sln add` every project (one command, all projects).
5. `dotnet build` — must succeed.
6. If a first feature was requested, immediately run **Mode 2** for that entity.
7. Report.

### Mode 2 — `add-feature`

For entity `{{Feature}}` (e.g. `Customer`):

1. **Domain**: `src/{{Solution}}.Domain/{{Feature}}s/{{Feature}}.cs` — POCO entity with a private parameterless ctor for EF, a public ctor for invariants, and behavior methods (avoid anemic models). Add domain events only if asked.
2. **Application**:
   - Port: `src/{{Solution}}.Application/{{Feature}}s/I{{Feature}}Repository.cs` (interface with CRUD methods that take `CancellationToken`).
   - DTOs: `Application/{{Feature}}s/Dtos/{{Feature}}Dto.cs`, `Create{{Feature}}Request.cs`, `Update{{Feature}}Request.cs`.
   - Use-case service: `Application/{{Feature}}s/{{Feature}}Service.cs` + interface `I{{Feature}}Service.cs`. Service depends on `I{{Feature}}Repository`, `IUnitOfWork`, `IMapper`. Pure orchestration — no EF references.
   - AutoMapper profile: `Application/{{Feature}}s/Mapping/{{Feature}}Profile.cs`.
   - FluentValidation validator (only if user asked for FluentValidation; otherwise rely on DataAnnotations + the validation factory).
3. **Infrastructure**:
   - EF configuration: `Infrastructure/Persistence/EntityConfigurations/{{Feature}}Configuration.cs` (implements `IEntityTypeConfiguration<{{Feature}}>`).
   - Repository adapter: `Infrastructure/Persistence/Repositories/{{Feature}}Repository.cs` (implements `I{{Feature}}Repository` using `AppDbContext`).
   - Register the DbSet on `AppDbContext`.
4. **Api**:
   - Controller: `Api/Controllers/{{Feature}}sController.cs` inheriting `BaseController`, injecting `I{{Feature}}Service`. Standard REST endpoints, returning DTOs only.
5. **Tests**:
   - `tests/{{Solution}}.UnitTests/{{Feature}}s/{{Feature}}ServiceTests.cs` — xUnit + NSubstitute, covers the service's happy path + one validation/edge case.

Template for the full slice is in [`references/templates/feature-slice.md`](references/templates/feature-slice.md).

After generating: `dotnet build` then `dotnet test`. Both must pass — apply the Step-4 proof-and-failure protocol (paste the green lines; the same step failing twice = stop and surface the verbatim error).

### Mode 3 — `add-worker`

For worker `{{Worker}}` (e.g. `EmailSender`):

1. Create `src/{{Solution}}.Workers.{{Worker}}/`:
   - `csproj` per [`references/templates/worker-csproj.md`](references/templates/worker-csproj.md).
   - `Program.cs` using `Host.CreateApplicationBuilder` per [`references/templates/worker-program.cs.md`](references/templates/worker-program.cs.md).
   - `Worker.cs` — `BackgroundService` subclass; loop driven by `stoppingToken`; respects graceful shutdown.
   - `appsettings.json` + `appsettings.Development.json`.
2. Reference `Application` + `Infrastructure` (never `Api`).
3. Add to `.sln`. `dotnet build`.
4. **No `while (true) { ... await Task.Delay(5s) }`** — use the SDK's receive loop (e.g. `await foreach (var msg in receiver.ReceiveMessagesAsync(stoppingToken))` for Service Bus, or `await queueClient.ReceiveMessagesAsync(maxMessages, ct: stoppingToken)` inside a `while (!stoppingToken.IsCancellationRequested)` loop).

## NuGet packages (resolve latest stable at scaffold time)

Look these up via context7 — do not hand-paste versions:

**Api project**
- `Microsoft.AspNetCore.Authentication.JwtBearer`
- `Microsoft.AspNetCore.OpenApi`
- `Swashbuckle.AspNetCore`
- `AutoMapper.Extensions.Microsoft.DependencyInjection` (or `AutoMapper` 13+ which self-registers)
- `Scrutor` (assembly-scanning DI)
- `Serilog.AspNetCore` + `Serilog.Sinks.Console` (only if user opted into Serilog)

**Application project**
- `MediatR` only if user explicitly asks for CQRS; default is plain service classes
- `FluentValidation` only if requested

**Infrastructure project**
- `Microsoft.EntityFrameworkCore.SqlServer`
- `Microsoft.EntityFrameworkCore.Design` (PrivateAssets="all")
- `Microsoft.EntityFrameworkCore.Tools` (PrivateAssets="all")
- `Microsoft.Data.SqlClient`
- `Azure.Storage.Blobs`, `Azure.Storage.Queues`, `Azure.Messaging.ServiceBus` (only if used)

**Worker projects**
- `Microsoft.Extensions.Hosting`
- Same Azure SDK packages as Infrastructure (only what the worker actually uses)

**Test projects**
- `Microsoft.NET.Test.Sdk`
- `xunit`, `xunit.runner.visualstudio`
- `NSubstitute` (preferred over Moq — cleaner API, actively maintained)
- `FluentAssertions`
- `Testcontainers.MsSql` (integration tests only)
- `Microsoft.AspNetCore.Mvc.Testing` (integration tests only)

## Final self-audit (mechanical — grep, don't recall)

The **Eliminate** list is easy to hold at file 1 and forgotten by file 30. After generating and before the final build, grep the generated tree — every command must return nothing:

```bash
grep -rn "Thread.Sleep\|while (true)" src/                        # polling-loop workers
grep -rnE "catch\s*(\(\s*Exception[^)]*\))?\s*\{\s*\}" src/       # swallowed exceptions
grep -rn "ExpandoObject\|DataRow\|SqlDataAdapter" src/            # sproc-era / reflection data access
grep -rn "GetService<" src/*/Program.cs                           # hosted services booted by hand
grep -rn "Newtonsoft" src/                                        # unless a dependency demanded it
grep -rln "public async Task" src/ | xargs grep -Ln "CancellationToken"   # async surface with no ct anywhere
grep -rn "System.Data.Entity\|\"EntityFramework\"" src/           # EF6 leaking into an EF Core solution
grep -rn "CreateDefaultBuilder" src/                               # mixed host-builder idioms
grep -rn "/// <summary>" src/                                      # XML doc blocks on internal members
```

A hit means fix it and re-run the grep — never rationalize it away or report it as acceptable.

## Verification checklist before reporting "done"

- [ ] `dotnet build` exits 0.
- [ ] `dotnet test` exits 0 (if tests were generated).
- [ ] No `.csproj` references violate the ONION rule. Concrete check: `grep "ProjectReference" src/*/*.csproj` — Domain shows zero hits, Application references only Domain, Api/Workers never reference each other.
- [ ] No file contains any pattern from the **Eliminate** list.
- [ ] `Program.cs` is under ~50 lines (everything else is in extension methods).
- [ ] Domain project's `.csproj` has zero `<ProjectReference>` entries.

If any check fails, fix before reporting. Don't claim success with a known-broken scaffold.

## Examples

### Example 1: Fresh solution

**User:** "Scaffold a new dotnet API project called `Acme.Billing` using my ONION patterns. Add a `Customer` feature too."

**Claude:**
1. Runs `dotnet --list-sdks`, checks context7 for current LTS, picks (e.g.) `net8.0`.
2. Reports chosen TFM + package versions; waits for confirmation if anything looks off.
3. Asks the Step-2 questions (auth flavor, workers, extras).
4. Generates the full solution + the `Customer` feature slice.
5. Runs `dotnet build` and `dotnet test`.
6. Reports the tree and the EF migration command.

### Example 2: Add a feature

**User:** "Add an `Invoice` feature end-to-end to the existing solution."

**Claude:** Runs Mode 2 only — generates Domain entity, Application port + service + DTOs, Infrastructure config + repository, Api controller, unit test. Builds and tests.

### Example 3: Add a worker

**User:** "Add a worker that processes the `print-jobs` Azure Storage queue."

**Claude:** Runs Mode 3 — generates `Workers.PrintJobs` project with a `BackgroundService` that receives messages with `stoppingToken`, calls into an Application service, deletes on success. Wires it into the .sln. Builds.

## Notes

- **Don't over-engineer**: don't add MediatR, CQRS, MassTransit, Polly, MinimalAPI conversions, Result<T> patterns, or domain events unless the user asks. Pragmatic > pure.
- **Don't rewrite the user's existing codebase** as part of this skill. This skill is for *new* scaffolds, not migrations. If the user wants a migration plan, that's a different conversation.
- **Multi-tenancy**: if the new project needs it, generate a `TenantContext` mirroring `IUserContext` and use EF Core query filters (`HasQueryFilter`) rather than per-tenant repositories.
- **Always quote the TFM and package versions you chose before writing files** — they are resolved at scaffold time, never hard-coded.
