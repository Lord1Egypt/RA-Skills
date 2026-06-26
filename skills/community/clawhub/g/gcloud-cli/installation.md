# Google Cloud CLI Installation

## Requirements

This skill requires:

- `gcloud` (Google Cloud CLI)

## Install and Verify

Install Google Cloud CLI from the official documentation:
https://docs.cloud.google.com/sdk/docs/install-sdk

Verify installation:
```bash
gcloud --version
```

## Initialize and Authenticate

Initialize CLI configuration:
```bash
gcloud init
```

Check active account and project:
```bash
gcloud config list --format='text(core.account,core.project)'
```

## Service Account Recommendation

Use a dedicated least-privilege service account for automation. Do not use personal or broad admin identities.

If needed, authenticate with a service account key or workload identity based on your organization policy.
