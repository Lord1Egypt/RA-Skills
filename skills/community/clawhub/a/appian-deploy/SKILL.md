---
name: appian-deploy
description: Deploy (import) an Appian package ZIP into an Appian environment. Use when the user wants to push, import, or deploy a package file to an Appian environment.
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Deploy

Imports a package ZIP into the Appian environment using the [v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Deploy_Package_API.html). Polls until a terminal status and prints a full object summary.

## Usage

```bash
node {baseDir}/scripts/index.js <zipPath> <deploymentName> [description] [customizationFilePath]
```

## Example

```bash
node {baseDir}/scripts/index.js "./appian-exports/MyPackage.zip" "Prod Release 1.2"
```

Exported packages are saved to `./appian-exports/` by `appian-export`.

Run `appian-inspectpkg` first to validate before deploying. If the environment requires approval, the deployment will return `PENDING_REVIEW` — check Appian Designer's Deploy view to approve.

## External endpoints

- `POST ${APPIAN_BASE_URL}/deployments` — triggers the import
- `GET ${APPIAN_BASE_URL}/deployments/{uuid}` — polls for completion

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, the script falls back to a `appian.json` file in the current working directory.
- The package ZIP is uploaded only to your configured Appian environment.
- No data is sent to any third-party service.
- No shell commands are executed; all operations use Node.js built-in APIs.
