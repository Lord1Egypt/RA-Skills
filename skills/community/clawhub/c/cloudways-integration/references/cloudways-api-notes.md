# Cloudways API Notes For This Integration

## Primary API behavior used

The current OpenClaw integration uses Cloudways account auth plus inventory discovery.

### Auth flow used
- OAuth-style access token request to:
  - `POST https://api.cloudways.com/api/v2/oauth/access_token`
- Request fields:
  - `email`
  - `api_key`
  - `grant_type=password`

### Inventory source used
The main inventory source is the server list endpoint family.

The implementation tries these candidates in order:
- `https://api.cloudways.com/api/v2/server`
- `https://api.cloudways.com/api/v1/server`
- `https://api.cloudways.com/api/v2/servers`
- `https://api.cloudways.com/api/v1/servers`

Applications are derived by flattening nested `apps[]` arrays from the server inventory response.

## Important modeling choice

This integration does **not** assume Cloudways inventory is a trustworthy complete source for live operational secrets.

Specifically:
- WordPress admin passwords should be treated as manual secure inputs
- App/server SSH secrets are stored separately in the vault
- DB Manager URL and DB credentials are stored separately in the vault

That split is intentional.

## API reference included in local development

The OpenClaw workspace already keeps a local Cloudways API reference copy at:
`/home/charl/.openclaw/workspace/skills/cloudways-wordpress-review/references/cloudways-api.md`

When maintaining this integration, use that reference for endpoint examples and shape confirmation.

## Safety note for packaging

Cloudways official docs and examples may include example credential-shaped fields in schemas. That is fine.

What must **not** be packaged from your live environment:
- real Cloudways email addresses
- real API keys
- real server ids or app ids from local notes unless intentionally redacted
- real DB manager URLs
- real database usernames/passwords/hosts
- any copied secrets from `secrets.json`
