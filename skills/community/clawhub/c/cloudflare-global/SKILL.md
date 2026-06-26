---
name: cloudflare-global
description: Cloudflare DNS and zone operations using a Global API Key. Use when the user needs to list, create, update, delete, export, or import DNS records, inspect zone settings or SSL mode, purge cache, inspect page rules or firewall rules, or work with Cloudflare tunnels using a Global API Key instead of a modern API token.
---

# Cloudflare Global

Use this skill to work with Cloudflare via the legacy Global API Key flow.

## Authentication

Read credentials from environment variables:

- `CLOUDFLARE_GLOBAL_API_KEY` — required
- `CLOUDFLARE_EMAIL` — required
- `CLOUDFLARE_ACCOUNT_ID` — required only for tunnel operations

Do not use Bearer auth for this flow.

## Workflow

1. Resolve the zone id for the domain.
2. List existing records when the user asks or when you need to avoid duplicates.
3. Create, update, delete, or export DNS records with the legacy headers:
   - `X-Auth-Email: $CLOUDFLARE_EMAIL`
   - `X-Auth-Key: $CLOUDFLARE_GLOBAL_API_KEY`
4. Keep DNS records `proxied: false` unless the user explicitly asks for proxying.
5. Use `ttl: 1` for Cloudflare auto TTL.
6. For tunnel operations, require `CLOUDFLARE_ACCOUNT_ID`.

## Script

Use `scripts/cf-global.sh` for repeatable Cloudflare operations.

## Available operations

- `verify`
- `zones` / `zones-list`
- `zone-get`
- `zone-id`
- `dns-list`
- `dns-create`
- `dns-update`
- `dns-delete`
- `dns-export`
- `dns-import`
- `settings-list`
- `setting-get`
- `setting-set`
- `ssl-get`
- `ssl-set`
- `cache-purge`
- `pagerules-list`
- `firewall-list`
- `tunnels-list`
- `tunnel-get`
- `tunnel-create`
- `tunnel-delete`
- `analytics`

## Publishing Notes

- This skill is safe to publish as-is: it does not contain embedded API keys, tokens, or account secrets.
- It relies on environment variables for credentials; users must provide their own values locally.
- Keep any examples, logs, and future edits free of real zone IDs, account IDs, emails, and record contents.
- Ensure `scripts/cf-global.sh` is included in the published package.
- The generated `dist/cloudflare-global.skill` file is a build artifact and should be regenerated before publishing if the source changes.

## Notes

- Prefer small, deterministic batches for bulk updates.
- If the API returns authorization or header-format errors, verify that the user provided a Global API Key and the correct Cloudflare account email.
