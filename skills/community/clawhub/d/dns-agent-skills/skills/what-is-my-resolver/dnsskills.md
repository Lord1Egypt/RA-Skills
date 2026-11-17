<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# What Is My DNS Resolver

Creates a unique lookup name and reports the resolver that queries it, with browser and manual workflow support.

## Discovery

- Identifier: `myresolver`
- Version: `v1`
- Category: Network identity
- Status: `live-specialized-flow`
- Access: `open`
- Human docs: https://dnsskills.md/skills/what-is-my-resolver
- Agent Markdown: https://dnsskills.md/skills/what-is-my-resolver.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/my-resolver

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `POST https://app.domainhelp.com/api/v1/myresolver/check`
  - Status: `live`
  - Response modes: `json`
- `GET https://app.domainhelp.com/api/v1/myresolver/result`
  - Status: `live`
  - Response modes: `json`

## Input Contract

Create a token with the check endpoint, query the returned hostname, then poll result with the token.

## Output Contract

Returns pending/resolved status, resolver IP, provider identification where available, DNSSEC validation check, and timing metadata.

## Errors

Token not found, token expired, or pending resolver result.

## Auth And Limits

Anonymous for initial rollout.

Public low-volume use. Token TTL and polling limits apply.

## Examples

### Requests

```text
POST /api/v1/myresolver/check
```

```text
GET /api/v1/myresolver/result?token=...
```

### Responses

```json
{"success":true,"status":"resolved","resolver_ip":"1.1.1.1"}
```

## FAQ

### Why is this a multi-step skill?

Resolver detection requires a DNS query to a unique hostname, so the skill creates a correlation token first.

## Related Skills

- [What Is My Public IP](https://dnsskills.md/skills/what-is-my-public-ip.md)
