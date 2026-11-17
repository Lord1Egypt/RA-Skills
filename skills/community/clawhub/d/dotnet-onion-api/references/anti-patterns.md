# Anti-patterns — what NOT to generate

Each item lists a common legacy pattern, why it's wrong, and what to do instead. The skill must never emit any of these in generated code.

## 1. Stored procedures as the dominant data path

**Anti-pattern:** Every repository calls a custom `Database`/`BaseData` wrapper around ADO.NET, executing `usp_Foo`-style stored procedures; business logic lives in SQL.

**Why bad:** Untyped, no refactoring tooling, untestable, no LINQ, no compile-time safety, hides domain logic in the DB.

**Do instead:** EF Core + LINQ for all reads/writes. Drop to `FromSqlInterpolated`/`ExecuteSqlInterpolated` *only* for legitimate perf hotspots or legacy sproc reuse, and use the interpolation form (parameters are bound automatically). Never use reflection-based parameter mapping.

## 2. `dynamic` / `ExpandoObject` parameter mapping

**Anti-pattern:** A `GetParameters(dynamic item)` helper that walks properties or ExpandoObject keys and switch-maps types to `SqlDbType`.

**Why bad:** Runtime errors, no IntelliSense, silent truncation (`SqlDbType.VarChar` defaults to 8000), terrible for code review.

**Do instead:** Strongly-typed request/DTO records. EF Core binds them.

## 3. Reflection-based `DataRow → object` mappers

**Anti-pattern:** A reflection-based `MapRowToObject`-style helper with a giant switch on `PropertyType.Name`, custom date parsing, swallowed exceptions on `SetValue`.

**Why bad:** Slow, ignores nullability, eats errors, can't be debugged.

**Do instead:** EF Core materializes entities. For ad-hoc projections, use `Select(x => new MyDto { ... })` in LINQ — fully typed.

## 4. EF6 on `netstandard2.1`

**Anti-pattern:** `EntityFramework 6.x` referenced from `netstandard2.1` libraries, EF Core nowhere.

**Why bad:** EF6 is maintenance-mode; no async-streaming, no compiled queries, no `IAsyncEnumerable`, no migrations bundles.

**Do instead:** **EF Core (latest stable for the chosen TFM)**, modern provider (`Microsoft.EntityFrameworkCore.SqlServer`).

## 5. Empty `catch {}`

**Anti-pattern:** Wrapping a SQL call (or any operation) in `try { ... } catch (Exception) { }` and returning a sentinel like `-1`.

**Why bad:** Bugs become silent. Failures masquerade as success.

**Do instead:** Let exceptions propagate to the centralized exception middleware. If a specific exception is genuinely recoverable, catch *that* type and log/handle explicitly.

## 6. Mutable public state on a service base class

**Anti-pattern:** `public class BaseService { public User User { get; set; } }` — a public setter on a scoped service.

**Why bad:** Anyone can stomp it. Risks cross-request leaks if lifetime gets botched.

**Do instead:** Inject `IUserContext` (scoped). No setters. The service reads `UserContext.UserId` etc. on demand.

## 7. Polling-loop workers as console apps

**Anti-pattern:**
```csharp
while (true)
{
    var msgs = await queueClient.ReceiveMessagesAsync(maxMessages: 1);
    if (msgs.Value.Length == 0) { await Task.Delay(5000); continue; }
    ...
}
```

**Why bad:** No graceful shutdown, no DI lifetime management, no health checks, can't be hosted alongside other services, no `IConfiguration` change tokens, no structured logging out of the box.

**Do instead:** `BackgroundService` with `protected override async Task ExecuteAsync(CancellationToken stoppingToken)`. Use `stoppingToken` in every `await`. Use `Host.CreateApplicationBuilder` + `services.AddHostedService<Worker>()`.

## 8. Booting hosted services with `serviceProvider.GetService<T>()`

**Anti-pattern:** Resolving a "listener" type from the service provider in `Program.cs` solely for its constructor side effects (starting a background loop).

**Why bad:** Brittle (forgets to resolve = silently dead). No lifetime hook. Can't unit test the hosted lifecycle.

**Do instead:** Implement `IHostedService` (or inherit `BackgroundService`) and register with `services.AddHostedService<MyListener>()`. The host owns start/stop.

## 9. Indiscriminate `Scoped` auto-registration

**Anti-pattern:** `RegisterAssemblyPublicNonGenericClasses(...).AsPublicImplementedInterfaces(ServiceLifetime.Scoped)` for every assembly, including ones that contain singletons.

**Why bad:** Singletons (Azure SDK clients, third-party notification clients, options) accidentally become scoped or vice versa. Memory leaks, perf issues, race conditions.

**Do instead:** Use Scrutor with lifetime selectors and exclude marker interfaces for non-scoped types:

```csharp
services.Scan(s => s
    .FromAssemblyOf<ApplicationAssemblyMarker>()
    .AddClasses(c => c.Where(t => t.Name.EndsWith("Service")))
        .AsImplementedInterfaces()
        .WithScopedLifetime());
```

Register singletons (Azure SDK clients, HttpClient factories, options) explicitly.

## 10. Newtonsoft.Json + PascalCase by default

**Anti-pattern:** `AddNewtonsoftJson(... new DefaultContractResolver())` with a TODO comment "use camel case later".

**Why bad:** PascalCase breaks JS/TS clients by convention; Newtonsoft is slower, larger, and not the framework default any more.

**Do instead:** Stick with System.Text.Json (default). Configure `JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase` if you want to be explicit (it's the default anyway in ASP.NET Core). Only add Newtonsoft for specific compatibility needs.

## 11. Missing `CancellationToken`

**Anti-pattern:** Async methods with no `CancellationToken` parameter, so client disconnects don't cancel server-side work.

**Do instead:** Every public async method takes `CancellationToken ct = default` as the **last** parameter and forwards it to every awaited call (`ToListAsync(ct)`, `SaveChangesAsync(ct)`, etc.). Controllers accept the framework-provided `HttpContext.RequestAborted` implicitly when you add `CancellationToken ct` to the action signature.

## 12. Per-tenant repository folders

**Anti-pattern:** `Repositories/TenantA/`, `Repositories/TenantB/` — branching tenant logic at the repository layer with parallel folders per customer.

**Why bad:** Doesn't scale, duplicates code, hides shared behavior, requires registering different implementations per tenant.

**Do instead:** One repository. Multi-tenant variations live behind a `ITenantStrategy` (or similar) port resolved at runtime, or via EF Core query filters tied to the current tenant ID.

## 13. Hard-coded multi-tenant fallback

**Anti-pattern:** A base data class constructor that assigns a literal default to the tenant/client identifier before reading claims (e.g. `DataContext.ClientId = "default";`).

**Why bad:** Silently routes anonymous/broken requests to a default tenant — security hole.

**Do instead:** `IUserContext.ClientId` either has a value or you reject the request. No magic defaults. If you legitimately have a public path, branch explicitly.

## 14. Commented-out dead code

**Anti-pattern:** Large `// var existing = await ...` blocks left in repository code "in case we need it later".

**Why bad:** Confuses readers, rots, never accurate again.

**Do instead:** Delete it. If you might need it later, that's what git is for.

## 15. Controllers that bypass the base class

**Anti-pattern:** A controller (often `AuthController`) inheriting `ControllerBase` directly to escape the `[Authorize]` default — losing every other cross-cutting filter in the process.

**Why bad:** Inconsistent cross-cutting concerns; easy to forget a filter.

**Do instead:** All controllers inherit `BaseController`. For public endpoints, decorate the *action* with `[AllowAnonymous]`.

## 16. Mixed data access (EF6 + Dapper + ADO.NET sprocs)

**Anti-pattern:** All three coexist in the same codebase, often in the same project.

**Why bad:** Three sets of conventions, three ways to fail, three connection-management stories.

**Do instead:** EF Core is the default. Dapper is acceptable as a perf escape hatch for read-heavy queries — register it side-by-side but don't sprinkle it everywhere.

## 17. Registering POCO config as a singleton

**Anti-pattern:** `services.AddSingleton(_ => builder.Configuration.GetSection("AppSettings").Get<AppSettings>())`.

**Why bad:** Doesn't react to `IOptionsMonitor` changes; couples consumers to the POCO; bypasses the options validation pipeline.

**Do instead:** `services.AddOptions<AppSettings>().Bind(config.GetSection("AppSettings")).ValidateDataAnnotations().ValidateOnStart();` — inject `IOptions<AppSettings>` (or `IOptionsSnapshot<T>` if you need reload).
