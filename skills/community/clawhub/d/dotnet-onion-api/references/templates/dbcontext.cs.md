# EF Core DbContext + Application ports + Infrastructure DI

## `src/{{Solution}}.Infrastructure/Persistence/AppDbContext.cs`

```csharp
using {{Solution}}.Application.Common;
using Microsoft.EntityFrameworkCore;
using System.Reflection;

namespace {{Solution}}.Infrastructure.Persistence;

public sealed class AppDbContext : DbContext
{
    private readonly IUserContext _userContext;

    public AppDbContext(DbContextOptions<AppDbContext> options, IUserContext userContext)
        : base(options)
    {
        _userContext = userContext;
    }

    // Add DbSet<T> properties per feature. Example:
    // public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        base.OnModelCreating(modelBuilder);
    }

    public override Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        // Hook: stamp audit columns from _userContext here if entities implement IAuditable.
        return base.SaveChangesAsync(ct);
    }
}
```

## `src/{{Solution}}.Application/Common/IUnitOfWork.cs`

```csharp
namespace {{Solution}}.Application.Common;

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}
```

## `src/{{Solution}}.Infrastructure/Persistence/UnitOfWork.cs`

```csharp
using {{Solution}}.Application.Common;

namespace {{Solution}}.Infrastructure.Persistence;

public sealed class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _db;
    public UnitOfWork(AppDbContext db) => _db = db;
    public Task<int> SaveChangesAsync(CancellationToken ct = default) => _db.SaveChangesAsync(ct);
}
```

## `src/{{Solution}}.Infrastructure/DependencyInjection.cs`

```csharp
using {{Solution}}.Application.Common;
using {{Solution}}.Infrastructure.Auth;
using {{Solution}}.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace {{Solution}}.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration config)
    {
        var connectionString = config.GetConnectionString("Default")
            ?? throw new InvalidOperationException("ConnectionStrings:Default is required.");

        services.AddDbContext<AppDbContext>(opt =>
            opt.UseSqlServer(connectionString, sql =>
            {
                sql.EnableRetryOnFailure();
                sql.CommandTimeout(60);
            }));

        services.AddScoped<IUnitOfWork, UnitOfWork>();
        services.AddScoped<IUserContext, UserContext>();

        // Auto-register concrete adapters whose interface lives in Application.
        // Convention: Infrastructure types named *Repository implement *Repository ports.
        services.Scan(s => s
            .FromAssemblyOf<AssemblyMarker>()
            .AddClasses(c => c.Where(t => t.Name.EndsWith("Repository")))
                .AsImplementedInterfaces()
                .WithScopedLifetime());

        return services;
    }
}

internal sealed class AssemblyMarker;
```

## `src/{{Solution}}.Application/DependencyInjection.cs`

```csharp
using Microsoft.Extensions.DependencyInjection;

namespace {{Solution}}.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddAutoMapper(cfg => cfg.AddMaps(typeof(ApplicationAssemblyMarker).Assembly));

        services.Scan(s => s
            .FromAssemblyOf<ApplicationAssemblyMarker>()
            .AddClasses(c => c.Where(t => t.Name.EndsWith("Service")))
                .AsImplementedInterfaces()
                .WithScopedLifetime());

        return services;
    }
}

public sealed class ApplicationAssemblyMarker;
```

## EF migrations

After scaffold, the user runs:

```bash
dotnet ef migrations add Initial \
  --project src/{{Solution}}.Infrastructure \
  --startup-project src/{{Solution}}.Api

dotnet ef database update \
  --project src/{{Solution}}.Infrastructure \
  --startup-project src/{{Solution}}.Api
```

Print this command in your final report so the user doesn't have to look it up.
