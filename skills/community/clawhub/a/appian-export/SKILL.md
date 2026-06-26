---
name: appian-export
description: Export an Appian application or package to a ZIP file by UUID. Use when the user wants to export, download, or back up an Appian application or package from an environment.
metadata:
  clawdbot:
    emoji: "📦"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Manager

Exports an Appian application or package as a ZIP using the [v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Export_Package_API.html).

## Usage

```bash
# Export an application
node {baseDir}/scripts/index.js <applicationUuid> [exportName]

# Export a specific package under an application
node {baseDir}/scripts/index.js <applicationUuid> --package <packageUuid> [exportName]
```

| Argument | Description |
|---|---|
| `applicationUuid` | UUID of the Appian application |
| `packageUuid` | UUID of the specific package (use `appian-listpkg` to list them) |
| `exportName` | Optional filename override; if omitted Appian's own name (with timestamp) is used |

## Examples

```bash
# Export full application
node {baseDir}/scripts/index.js _a-0000de15-1f1c-8000-5130-010000010000_12559

# Export a specific package under that application
node {baseDir}/scripts/index.js _a-0000de15-1f1c-8000-5130-010000010000_12559 --package _a-0007ee60-0f3e-8000-e0f6-01ef9001ef90_137916
```

The script polls until `COMPLETED` and saves the ZIP to `~/appian-exports/`. When running inside a container (where the working directory differs from `~/appian-exports/`), the ZIP is also copied to `appian-exports/` inside the current working directory for easy access.

## After running

Always report back to the user:
- The **ZIP path** printed after `ZIP path:` (primary location)
- The **Copied to** path if printed (accessible in `appian-exports/` inside the current working directory)
- The file **size** in KB

## External endpoints

- `POST ${APPIAN_BASE_URL}/deployments` — triggers the export
- `GET ${APPIAN_BASE_URL}/deployments/{uuid}` — polls for completion
- `GET <packageZip URL>` — downloads the resulting ZIP

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, the script falls back to a `appian.json` file in the current working directory.
- No data is sent to any third-party service — all requests go to your configured Appian environment.
- The exported ZIP is written locally to `~/appian-exports/` and never uploaded anywhere.
- No shell commands are executed; all operations use Node.js built-in APIs.
