---
name: appian-deploymtstatus
description: Check the status of an Appian deployment by UUID and optionally download its artifacts (log, package ZIP). Use after appian-export or appian-deploy to monitor progress or retrieve results.
metadata:
  clawdbot:
    emoji: "📡"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Status

Retrieves the current status and artifact URLs for any Appian deployment using the [v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Get_Deployment_Results_API.html). Supports optional polling and artifact download.

## Usage

```bash
node {baseDir}/scripts/index.js <deploymentUuid> [--wait] [--download-log] [--download-zip]
```

| Flag | Description |
|---|---|
| `--wait` | Poll until a terminal status is reached |
| `--download-log` | Save the deployment log to `~/appian-exports/` |
| `--download-zip` | Save the package ZIP (export deployments only) to `~/appian-exports/` |

## Examples

```bash
# Check immediately
node {baseDir}/scripts/index.js 208d489c-6f74-45f7-a48a-f0887fefeca9

# Wait for completion and download log
node {baseDir}/scripts/index.js 208d489c-6f74-45f7-a48a-f0887fefeca9 --wait --download-log
```

## External endpoints

- `GET ${APPIAN_BASE_URL}/deployments/{uuid}` — fetches deployment status
- Artifact URLs returned by the API (log, ZIP) — downloaded only when flags are passed

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, the script falls back to an `appian.json` file in the current working directory.
- Artifacts are saved only to `~/appian-exports/` — nothing is uploaded or sent to third parties.
- No shell commands are executed; all operations use Node.js built-in APIs.
