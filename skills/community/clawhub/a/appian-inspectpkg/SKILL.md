---
name: appian-inspectpkg
description: Inspect an Appian package ZIP against the target environment to identify errors or warnings before deploying. Use before appian-deploy to validate a package.
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Inspect

Runs a pre-deployment inspection of a package ZIP against the Appian environment using the [v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Inspect_Package_API.html). Returns expected object counts and any errors or warnings.

> A `FAILED` inspection status indicates a system error, not an invalid package. Errors and warnings are predictions about what deploying will do, not hard blockers.

## Usage

```bash
node {baseDir}/scripts/index.js <zipPath> [customizationFilePath]
```

## Example

```bash
node {baseDir}/scripts/index.js "./appian-exports/MyPackage.zip"
```

Exported packages are saved to `./appian-exports/` by `appian-export`.

## External endpoints

- `POST ${APPIAN_BASE_URL}/inspections` — submits the package for inspection
- `GET ${APPIAN_BASE_URL}/inspections/{uuid}` — polls for results

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, the script falls back to a `appian.json` file in the current working directory.
- The package ZIP is uploaded only to your configured Appian environment.
- No data is sent to any third-party service.
- No shell commands are executed; all operations use Node.js built-in APIs.
