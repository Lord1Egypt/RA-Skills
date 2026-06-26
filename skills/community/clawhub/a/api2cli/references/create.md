# Create a CLI Scaffold

## Command

```bash
npx api2cli create <app> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `<app>` | API/app name (e.g. typefully, dub) | required |
| `--base-url <url>` | API base URL | `https://api.example.com` |
| `--auth-type <type>` | bearer, api-key, basic, custom | `bearer` |
| `--auth-header <name>` | Auth header name | `Authorization` |
| `--docs <url>` | API docs URL | - |
| `--openapi <url>` | OpenAPI/Swagger spec URL | - |
| `--force` | Overwrite existing CLI | `false` |

## Examples

```bash
npx api2cli create typefully --base-url https://api.typefully.com --auth-type bearer
npx api2cli create dub --openapi https://api.dub.co/openapi.json
npx api2cli create my-api --docs https://docs.example.com/api
```

## What gets generated

Creates `~/.cli/<app>-cli/` with:

```
~/.cli/<app>-cli/
  src/
    index.ts              # Entry point - register resources here
    lib/
      client.ts           # HTTP client with retry/backoff
      auth.ts             # Token management (chmod 600)
      output.ts           # Multi-format output (text, json, csv, yaml)
      errors.ts           # Error handling with suggestions
      logger.ts           # Logging (suppressed in --json mode)
    resources/
      example.ts          # Example resource to copy
  skills/
    <app>-cli/
      SKILL.md            # AgentSkill template (update after implementing)
  README.md               # README template (update after implementing)
  package.json
  tsconfig.json
```

## After create

1. Edit resources in `src/resources/`
2. Build: `npx api2cli bundle <app>`
3. Link: `npx api2cli link <app>`
4. Auth: `<app>-cli auth set "your-token"`
