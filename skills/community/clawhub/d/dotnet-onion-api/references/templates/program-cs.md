# `src/{{Solution}}.Api/Program.cs`

Thin top-level program; all wiring is in extension methods.

```csharp
using {{Solution}}.Api.Extensions;
using {{Solution}}.Api.Middlewares;
using {{Solution}}.Application;
using {{Solution}}.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration)
    .AddApiServices(builder.Configuration)
    .AddJwtAuth(builder.Configuration)
    .AddSwaggerDocs()
    .AddCorsPolicies(builder.Configuration);

var app = builder.Build();

app.UseCustomExceptionHandler();

if (app.Environment.IsDevelopment() || app.Environment.IsStaging())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();

// Expose Program for WebApplicationFactory<Program> in integration tests.
public partial class Program;
```

## `Extensions/ApiBehaviorExtensions.cs`

```csharp
using {{Solution}}.Api.Models;
using Microsoft.AspNetCore.Mvc;

namespace {{Solution}}.Api.Extensions;

public static class ApiBehaviorExtensions
{
    public static IServiceCollection AddApiServices(this IServiceCollection services, IConfiguration config)
    {
        services.AddControllers()
            .ConfigureApiBehaviorOptions(options =>
            {
                options.InvalidModelStateResponseFactory = ctx =>
                {
                    var errors = ctx.ModelState
                        .Where(e => e.Value?.Errors.Count > 0)
                        .SelectMany(x => x.Value!.Errors)
                        .Select(x => x.ErrorMessage)
                        .ToArray();

                    return new BadRequestObjectResult(new ApiValidationErrorResponse
                    {
                        Errors = errors,
                        Message = "One or more validation errors occurred."
                    });
                };
            });

        services.AddEndpointsApiExplorer();
        services.AddHttpContextAccessor();
        return services;
    }
}
```

## `Extensions/AuthExtensions.cs`

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

namespace {{Solution}}.Api.Extensions;

public static class AuthExtensions
{
    public static IServiceCollection AddJwtAuth(this IServiceCollection services, IConfiguration config)
    {
        var secret = config["AppSettings:SecretToken"]
            ?? throw new InvalidOperationException("AppSettings:SecretToken is required.");

        services
            .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
            .AddJwtBearer(options =>
            {
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secret)),
                    ValidateIssuer = false,
                    ValidateAudience = false,
                };
            });

        services.AddAuthorization();
        return services;
    }
}
```

## `Extensions/SwaggerExtensions.cs`

```csharp
using Microsoft.OpenApi.Models;

namespace {{Solution}}.Api.Extensions;

public static class SwaggerExtensions
{
    public static IServiceCollection AddSwaggerDocs(this IServiceCollection services)
    {
        services.AddSwaggerGen(c =>
        {
            c.SwaggerDoc("v1", new OpenApiInfo { Title = "{{Solution}} API", Version = "v1" });

            var jwt = new OpenApiSecurityScheme
            {
                Name = "Authorization",
                Type = SecuritySchemeType.Http,
                Scheme = "bearer",
                BearerFormat = "JWT",
                In = ParameterLocation.Header,
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" }
            };
            c.AddSecurityDefinition("Bearer", jwt);
            c.AddSecurityRequirement(new OpenApiSecurityRequirement { [jwt] = Array.Empty<string>() });
        });

        return services;
    }
}
```

## `Extensions/CorsExtensions.cs`

```csharp
namespace {{Solution}}.Api.Extensions;

public static class CorsExtensions
{
    public static IServiceCollection AddCorsPolicies(this IServiceCollection services, IConfiguration config)
    {
        var origins = config.GetSection("AppSettings:AllowedOrigins").Get<string[]>() ?? [];

        services.AddCors(options =>
        {
            options.AddDefaultPolicy(p => p
                .WithOrigins(origins)
                .AllowAnyHeader()
                .AllowAnyMethod()
                .AllowCredentials());
        });

        return services;
    }
}
```
