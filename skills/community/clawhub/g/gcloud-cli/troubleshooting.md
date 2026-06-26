# Google Cloud CLI Troubleshooting

## Authentication Issues

### `UNAUTHENTICATED` or credential errors

- Re-authenticate if needed:
  ```bash
  gcloud auth login
  ```
- Confirm active identity and project:
  ```bash
  gcloud config list --format='text(core.account,core.project)'
  ```
- Confirm account has required IAM roles.

## Permission Denied (`403`)

- The active identity lacks permissions for the operation.
- Verify IAM role bindings and organization policy constraints.
- Validate whether service account impersonation is being used.

## Resource Not Found (`404`)

- Wrong project, region, zone, or resource name.
- Resource exists in a different project or location.
- Check current defaults:
  ```bash
  gcloud config list
  ```

## API Not Enabled

Some commands fail if the required service API is disabled.

- Enable required services as needed:
  ```bash
  gcloud services enable SERVICE_API_NAME
  ```

## Command Syntax Errors

- Always inspect current help for the command group:
  ```bash
  gcloud <GROUP> --help
  gcloud <GROUP> <SUBGROUP> --help
  ```
- Do not rely on memorized flags across CLI versions.

## Quick Debug Checklist

1. Confirm active account/project: `gcloud config list --format='text(core.account,core.project)'`
2. Confirm target location defaults: `gcloud config list`
3. Check command syntax with `--help`
4. Verify IAM permissions for the identity in use
5. Confirm required APIs are enabled
