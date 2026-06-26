# Provider Matrix - Domain Registration

Use this matrix to choose execution path before any domain lifecycle action.

| Provider | API Availability | Dashboard URL | Auth Model | Notes |
|----------|------------------|---------------|------------|-------|
| GoDaddy | Public Domains API (`api.godaddy.com`) | `sso.godaddy.com` | API key + secret | API supports broad domain lifecycle operations |
| Namecheap | XML API (`api.namecheap.com/xml.response`) | `ap.www.namecheap.com` | API user + key + whitelisted client IP | DNS replace actions require full host set |
| Route 53 Domains | AWS API (`route53domains.us-east-1.amazonaws.com`) | `console.aws.amazon.com` | IAM credentials or role | Favor least-privilege IAM for domain actions |
| Cloudflare Registrar | Partial API for DNS context; registrar lifecycle mostly dashboard | `dash.cloudflare.com` | API token + dashboard account | Registration and transfer lifecycle is often dashboard-led |
| Google Cloud Domains | Cloud Domains API (`domains.googleapis.com`) | `console.cloud.google.com` | Google Cloud IAM | Useful for portfolio operations in GCP projects |
| Squarespace Domains | No public registrar API | `account.squarespace.com` | Dashboard account | Dashboard-first path for Google Domains migrations |
| Dynadot | Public API (`api.dynadot.com`) | `dynadot.com` | API key | Good fit for scripted portfolio operations |
| Porkbun | Public JSON API (`porkbun.com/api/json/v3`) | `porkbun.com` | API key + secret | API-first for registration and DNS operations |
| Name.com | Public REST API (`api.name.com`) | `name.com` | API token / basic auth | Supports registration, transfer, and DNS workflows |
| Gandi | Public v5 API (`api.gandi.net`) | `gandi.net` | Personal access token | EU-focused registrar with API coverage |
| OVHcloud Domains | Public API (`api.ovh.com`) | `www.ovh.com/manager` | API key + app key + app secret | Strong regional support and signed API pattern |
| OpenSRS / Enom | Reseller APIs (`api.opensrs.com`, provider-specific endpoints) | Reseller panels | Reseller credentials | Useful for agencies and wholesale portfolios |

## Decision Rules

- If API is available and complete for the task, prefer API for repeatability and auditability.
- If API is partial or unavailable, use dashboard with explicit checkpoints.
- For unknown provider capabilities, run read-only checks first and document constraints.

## Preflight Checklist

1. Confirm provider account and environment.
2. Confirm API credentials or dashboard access path.
3. Confirm whether action has billing impact.
4. Confirm transfer lock, auth code, or DNS dependency requirements.
5. Log planned action in `changes.md` before execution.
