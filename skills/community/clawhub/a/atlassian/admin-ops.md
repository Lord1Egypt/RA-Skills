# Cloud Admin, Compass, Statuspage, Opsgenie, and GraphQL

## Cloud Admin REST APIs

Base URL:
`https://api.atlassian.com/admin`

Families:
- organizations
- user management
- user provisioning (SCIM)
- data loss prevention
- admin control
- API access

Quick example:
```bash
curl -s "https://api.atlassian.com/admin/v2/orgs/<org_id>/users/invite" \
  -H "Authorization: Bearer <admin_api_key>" \
  -H "Content-Type: application/json"
```

Admin gotchas:
- You need organization context and an admin API key.
- Current docs include active v1 to v2 migrations and 2026 deprecations for some user and group flows.
- Org-wide automation is high impact; preview targets before mutation.

## Compass REST and GraphQL

REST base:
`https://api.atlassian.com/compass/cloud/{cloudId}`

GraphQL:
`https://api.atlassian.com/graphql` or tenant/product gateway

Use for:
- components, scorecards, metrics, events, and catalog relationships
- richer reads through the Atlassian GraphQL Gateway

Compass gotchas:
- Many workflows require `cloudId`, ARIs, or GraphQL identifiers.
- Official docs say GraphQL exposes more Compass functionality than REST alone.
- Forge is the normal way to build product-side Compass integrations.

## Statuspage API

Base URL:
`https://api.statuspage.io/v1`

Use for:
- pages, incidents, incident updates
- components, metrics, and subscribers

Quick example:
```bash
curl -s "https://api.statuspage.io/v1/pages/<page_id>/incidents" \
  -H "Authorization: OAuth <statuspage_api_key>"
```

Statuspage gotchas:
- Official rate limit is 1 request per second per token.
- Most writes are nested objects like `incident[...]` or `component[...]`.
- Page IDs and component IDs are required almost everywhere.

## Opsgenie API

Base URL:
`https://api.opsgenie.com` or `https://api.eu.opsgenie.com`

Use for:
- alerts, schedules, on-call rotations, escalation policies, integrations

Opsgenie gotchas:
- Region matters; EU traffic uses a different host.
- Official docs now flag Opsgenie as approaching end of support and point many users toward Jira Service Management or Compass migrations.

## Atlassian GraphQL Gateway

Use GraphQL when:
- the task spans multiple Atlassian products
- Compass or graph objects are easier to query by relationship
- the REST API is missing the needed read shape

Gateway gotchas:
- Tenanted products use `https://{subdomain}.atlassian.net/gateway/api/graphql`.
- Non-tenanted products can use product-specific gateways such as Bitbucket or Trello.
- Some products, including Opsgenie, may not register the same gateway route.

## Official Docs

- Cloud Admin: https://developer.atlassian.com/cloud/admin/rest-apis/
- Organizations REST API: https://developer.atlassian.com/cloud/admin/organization/rest/intro/
- Compass REST: https://developer.atlassian.com/cloud/compass/rest/v2/intro/
- Compass GraphQL: https://developer.atlassian.com/cloud/compass/graphql/
- Statuspage: https://developer.statuspage.io/
- Opsgenie: https://docs.opsgenie.com/docs/api-overview
- GraphQL: https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/
