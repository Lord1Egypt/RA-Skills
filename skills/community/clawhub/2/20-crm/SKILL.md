---
name: twenty-crm
description: Interact with Twenty CRM (self-hosted) via REST/GraphQL.
metadata: {"clawdbot":{"emoji":"🗂️","os":["darwin","linux"],"requirements":{"env":["TWENTY_BASE_URL","TWENTY_API_KEY"],"binaries":["curl","python3"]}}}
---

# Twenty CRM

Interact with your self-hosted Twenty instance via REST and GraphQL.

## Config

Set these env vars directly, or place them in `config/twenty.env`:

- `TWENTY_BASE_URL` (e.g. `https://crm.example.com` or `http://localhost:3000`)
- `TWENTY_API_KEY` (Bearer token)

Scripts auto-load `config/twenty.env` relative to this skill. You can override the path with `TWENTY_CONFIG_FILE`.

## Runtime Requirements

- `curl`
- `python3`

## Commands

### Low-level helpers

- REST GET: `skills/twenty-crm/scripts/twenty-rest-get.sh "/companies" 'filter={"name":{"ilike":"%acme%"}}' "limit=10" "offset=0"`
- REST POST: `skills/twenty-crm/scripts/twenty-rest-post.sh "/companies" '{"name":"Acme"}'`
- REST PATCH: `skills/twenty-crm/scripts/twenty-rest-patch.sh "/companies/<id>" '{"employees":550}'`
- REST DELETE: `skills/twenty-crm/scripts/twenty-rest-delete.sh "/companies/<id>"`

- GraphQL: `skills/twenty-crm/scripts/twenty-graphql.sh 'query { companies(limit: 5) { totalCount } }'`

### Common objects (examples)

- Create company: `skills/twenty-crm/scripts/twenty-create-company.sh "Acme" "acme.com" 500`
- Find companies by name: `skills/twenty-crm/scripts/twenty-find-companies.sh "acme" 10`

## Notes

- Twenty supports both REST (`/rest/...`) and GraphQL (`/graphql`).
- Object names/endpoints can differ depending on your workspace metadata and Twenty version.
- Auth tokens can be short-lived depending on your setup; refresh if you get `401`.

## Security

- Keep `TWENTY_API_KEY` out of git and avoid storing it in shared/world-readable files.
- If you use `config/twenty.env`, prefer restrictive permissions (for example `chmod 600 config/twenty.env`).
- Pass REST query parameters as separate `key=value` arguments; do not append raw query strings to REST paths.
