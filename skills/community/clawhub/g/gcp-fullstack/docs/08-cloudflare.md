> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Part 10: Cloudflare DNS, CDN, and Security

### API Base

```
https://api.cloudflare.com/client/v4
```

Auth header: `Authorization: Bearer $CLOUDFLARE_API_TOKEN`

### DNS Setup for Cloud Run

Get the Cloud Run service URL, then create the DNS records:

```bash
# Get Cloud Run URL
SERVICE_URL=$(gcloud run services describe <service-name> --region $GCP_REGION --format 'value(status.url)')

# Add CNAME record pointing custom domain to Cloud Run
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "<subdomain>",
    "content": "<service-name>-<hash>-<region>.a.run.app",
    "ttl": 1,
    "proxied": true
  }' | jq .
```

### Domain Mapping on Cloud Run

```bash
# Map custom domain to Cloud Run service
gcloud run domain-mappings create \
  --service <service-name> \
  --domain <your-domain.com> \
  --region $GCP_REGION

# Verify domain ownership
gcloud run domain-mappings describe \
  --domain <your-domain.com> \
  --region $GCP_REGION
```

### SSL/TLS Configuration

```bash
# Set SSL to Full (Strict) — required when proxying through Cloudflare
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}' | jq .

# Enable Always Use HTTPS
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/always_use_https" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}' | jq .
```

### Rate Limiting

```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/rulesets/phases/http_ratelimit/entrypoint" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [{
      "expression": "(http.request.uri.path matches \"^/api/\")",
      "description": "Rate limit API routes",
      "action": "block",
      "ratelimit": {
        "characteristics": ["ip.src"],
        "period": 60,
        "requests_per_period": 100,
        "mitigation_timeout": 600
      }
    }]
  }' | jq .
```

### Cache Purge After Deploy

```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything": true}' | jq .
```

### Bot Fight Mode

```bash
curl -s -X PUT \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/bot_management" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"fight_mode": true}' | jq .
```

### Standard Setup for New Projects (Cloudflare)

1. Add CNAME record pointing to Cloud Run service URL.
2. Set SSL to Full (Strict).
3. Enable Always Use HTTPS.
4. Add rate limiting for `/api/*` routes.
5. Enable Bot Fight Mode.
6. Set browser cache TTL to 4 hours.
7. Purge cache after every production deployment.
