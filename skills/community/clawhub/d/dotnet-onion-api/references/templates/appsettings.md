# `appsettings.json` templates

## `src/{{Solution}}.Api/appsettings.json`

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\MSSQLLocalDB;Database={{Solution}};Trusted_Connection=True;TrustServerCertificate=True"
  },
  "AppSettings": {
    "SecretToken": "REPLACE_ME_WITH_A_LONG_RANDOM_STRING_AT_LEAST_32_CHARS",
    "AllowedOrigins": [ "https://localhost:5173" ]
  }
}
```

## `src/{{Solution}}.Api/appsettings.Development.json`

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

## Strongly-typed binding (in `AddApiServices`)

```csharp
services.AddOptions<AppSettings>()
    .Bind(config.GetSection("AppSettings"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

## `AppSettings.cs` POCO (lives in Api project — Api is the only consumer of API-specific settings)

```csharp
using System.ComponentModel.DataAnnotations;

namespace {{Solution}}.Api.Configuration;

public sealed class AppSettings
{
    [Required, MinLength(32)]
    public string SecretToken { get; set; } = string.Empty;

    public string[] AllowedOrigins { get; set; } = Array.Empty<string>();
}
```

## Secrets

In `Development`, the `SecretToken` must come from User Secrets, not `appsettings.Development.json` (don't commit secrets):

```bash
dotnet user-secrets init --project src/{{Solution}}.Api
dotnet user-secrets set "AppSettings:SecretToken" "<long-random-string>" --project src/{{Solution}}.Api
```

In `Production`, set via environment variables or your secret store (Key Vault, etc.). The double-underscore form binds to nested keys:

```
AppSettings__SecretToken=...
ConnectionStrings__Default=...
```
