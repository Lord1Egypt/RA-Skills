---
name: appian-listpkg
description: List all packages for an Appian application by UUID. Use when the user wants to see what packages exist in an application, or to find a package UUID before inspecting or deploying.
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Packages

Lists all packages for an Appian application, including name, UUID, object count, and timestamps. Uses the [v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Package_Management_API.html).

## Usage

```bash
node {baseDir}/scripts/index.js <applicationUuid>
```

## Example

```bash
node {baseDir}/scripts/index.js _a-0007ee60-0f3e-8000-e0f6-01ef9001ef90_137916
```

Use the returned package UUID with `appian-inspectpkg` before deploying, or with `appian-export` to export a specific package.

## External endpoints

- `GET ${APPIAN_BASE_URL}/applications/{uuid}/packages`

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, the script falls back to a `appian.json` file in the current working directory.
- No data is written or uploaded — read-only API call.
- No shell commands are executed; all operations use Node.js built-in APIs.
