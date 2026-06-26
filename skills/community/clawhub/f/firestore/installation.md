# Firestore Installation

## Requirements

This skill requires two command-line tools to be installed:

1. **curl** - for making HTTP requests to the Firestore REST API
2. **gcloud CLI** - for authentication token generation

## Install and Verify

### curl

`curl` is typically pre-installed on macOS and most Linux distributions.

Verify installation:
```bash
curl --version
```

### Google Cloud CLI

Install from the official Google Cloud SDK documentation:
https://docs.cloud.google.com/sdk/docs/install-sdk

Verify installation:
```bash
gcloud --version
```

## Authenticate and Configure Project

After installation, authenticate and set the active project:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

Check active account and project:
```bash
gcloud config list --format='text(core.account,core.project)'
```

## Access Token

Before any Firestore API request, generate a fresh access token:
```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
```

The token is short-lived (typically around 1 hour). Regenerate it if requests return `401 Unauthorized`.
