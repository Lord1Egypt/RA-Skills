# CLI Setup

AutoPostOnline works well with terminal-based agents and automation scripts.

## Environment

```bash
export POSTIZ_API_URL="https://app.autopostonline.com/api"
export POSTIZ_API_KEY="your_api_key"
```

## Test

```bash
curl -sS \
  -H "Authorization: Bearer $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

## Safe shell script pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${POSTIZ_API_URL:?missing POSTIZ_API_URL}"
: "${POSTIZ_API_KEY:?missing POSTIZ_API_KEY}"

curl -sS \
  -H "Authorization: Bearer $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

## Autonomous agent shell prompt

```text
Use AutoPostOnline as the publishing backend. Read POSTIZ_API_URL and POSTIZ_API_KEY from the environment. List integrations first. Publish only inside the approved campaign rules.
```

## Secret storage

Use:

- environment variables
- GitHub Actions secrets
- Docker secrets
- AWS Secrets Manager
- GCP Secret Manager
- HashiCorp Vault
- 1Password CLI

Never commit API keys.
