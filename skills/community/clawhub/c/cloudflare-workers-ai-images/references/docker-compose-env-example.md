# Docker Compose environment example

Pass Cloudflare credentials into the OpenClaw container via `docker-compose.yml` or `compose.yaml`.

```yaml
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    environment:
      CF_ACCOUNT_ID: "your_cloudflare_account_id"
      CF_API_TOKEN: "your_cloudflare_api_token"
```

## Minimal token scope

Create a Cloudflare API token that can call Workers AI for the target account.
Prefer the least privilege that still allows AI inference.
If Cloudflare changes permission names, select the Workers AI / AI inference related permission for that account.

## Verify inside container

```bash
docker compose exec openclaw env | grep '^CF_'
```

Expected output should include both variables.
