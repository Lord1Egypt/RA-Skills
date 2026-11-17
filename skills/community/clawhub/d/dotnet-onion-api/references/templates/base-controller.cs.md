# `src/{{Solution}}.Api/Controllers/BaseController.cs`

```csharp
using {{Solution}}.Application.Common;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace {{Solution}}.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
[Produces("application/json")]
public abstract class BaseController : ControllerBase
{
    protected readonly IUserContext UserContext;

    protected BaseController(IUserContext userContext)
    {
        UserContext = userContext;
    }
}
```

# `src/{{Solution}}.Application/Common/IUserContext.cs`

```csharp
namespace {{Solution}}.Application.Common;

/// Provides per-request user identity. Resolved per scope.
public interface IUserContext
{
    int UserId { get; }
    string UserName { get; }
    string? ClientId { get; }
    bool IsAuthenticated { get; }
    IReadOnlyCollection<string> Roles { get; }
}
```

# `src/{{Solution}}.Infrastructure/Auth/UserContext.cs`

```csharp
using System.Security.Claims;
using {{Solution}}.Application.Common;
using Microsoft.AspNetCore.Http;

namespace {{Solution}}.Infrastructure.Auth;

public sealed class UserContext : IUserContext
{
    private readonly IHttpContextAccessor _accessor;

    public UserContext(IHttpContextAccessor accessor) => _accessor = accessor;

    private ClaimsPrincipal? User => _accessor.HttpContext?.User;

    public bool IsAuthenticated => User?.Identity?.IsAuthenticated ?? false;

    public int UserId =>
        int.TryParse(User?.FindFirstValue(ClaimTypes.NameIdentifier), out var id) ? id : 0;

    public string UserName => User?.FindFirstValue(ClaimTypes.Name) ?? string.Empty;

    public string? ClientId => User?.FindFirstValue("client_id");

    public IReadOnlyCollection<string> Roles =>
        User?.FindAll(ClaimTypes.Role).Select(c => c.Value).ToArray() ?? Array.Empty<string>();
}
```

# `src/{{Solution}}.Api/Models/ApiException.cs`

```csharp
namespace {{Solution}}.Api.Models;

public sealed record ApiException(int StatusCode, string Message, string? Detail = null);
```

# `src/{{Solution}}.Api/Models/ApiValidationErrorResponse.cs`

```csharp
namespace {{Solution}}.Api.Models;

public sealed class ApiValidationErrorResponse
{
    public string Message { get; set; } = string.Empty;
    public string[] Errors { get; set; } = Array.Empty<string>();
}
```
