# Exception handler middleware

## `src/{{Solution}}.Api/Middlewares/ExceptionHandlerMiddleware.cs`

```csharp
using System.Net;
using System.Text.Json;
using {{Solution}}.Api.Models;
using {{Solution}}.Application.Common.Exceptions;

namespace {{Solution}}.Api.Middlewares;

public sealed class ExceptionHandlerMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlerMiddleware> _logger;
    private readonly IWebHostEnvironment _env;

    public ExceptionHandlerMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlerMiddleware> logger,
        IWebHostEnvironment env)
    {
        _next = next;
        _logger = logger;
        _env = env;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleAsync(context, ex);
        }
    }

    private async Task HandleAsync(HttpContext context, Exception ex)
    {
        var (status, message) = ex switch
        {
            NotFoundException nf  => ((int)HttpStatusCode.NotFound, nf.Message),
            ValidationException v => ((int)HttpStatusCode.BadRequest, v.Message),
            ConflictException c   => ((int)HttpStatusCode.Conflict, c.Message),
            UnauthorizedAccessException u => ((int)HttpStatusCode.Unauthorized, u.Message),
            _ => ((int)HttpStatusCode.InternalServerError, "An unexpected error occurred.")
        };

        if (status >= 500)
        {
            _logger.LogError(ex, "Unhandled exception: {Message}", ex.Message);
        }
        else
        {
            _logger.LogWarning(ex, "Handled exception: {Message}", ex.Message);
        }

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = status;

        var includeDetail = _env.IsDevelopment() || _env.IsStaging();
        var payload = new ApiException(status, message, includeDetail ? ex.StackTrace : null);

        await context.Response.WriteAsync(JsonSerializer.Serialize(payload, new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        }));
    }
}

public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseCustomExceptionHandler(this IApplicationBuilder app) =>
        app.UseMiddleware<ExceptionHandlerMiddleware>();
}
```

## `src/{{Solution}}.Application/Common/Exceptions/*.cs`

```csharp
namespace {{Solution}}.Application.Common.Exceptions;

public class NotFoundException : Exception
{
    public NotFoundException(string entity, object key)
        : base($"{entity} with key '{key}' was not found.") { }
}

public class ValidationException : Exception
{
    public ValidationException(string message) : base(message) { }
}

public class ConflictException : Exception
{
    public ConflictException(string message) : base(message) { }
}
```
