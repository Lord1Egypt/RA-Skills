<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# Link Expander / Redirect Chain

Follows a URL through its HTTP redirect chain and reports status codes, redirect targets, response headers, bounded payload samples, and HTML metadata for each hop.

## Discovery

- Identifier: `redirectchain`
- Version: `v1`
- Category: Domain intelligence
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/redirect-chain
- Agent Markdown: https://dnsskills.md/skills/redirect-chain.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/redirect-chain

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `GET/POST https://app.domainhelp.com/api/v1/redirect-chain`
  - Status: `live`
  - Response modes: `json`
- `GET/POST https://app.domainhelp.com/api/v1/link-expander`
  - Status: `live-alias`
  - Response modes: `json`

## Input Contract

Provide url, or link as an alias, as an http or https URL up to 2048 characters. If no scheme is supplied, https is assumed. Optional max_hops may be set from 1 to 20 and defaults to 10. Only standard HTTP and HTTPS ports are supported, and private or reserved network targets are blocked.

## Output Contract

Returns normalized_url, final_url, hop_count, redirect_count, terminal_status_code, terminated_reason, verdict, summary, and a chain array. Each hop includes URL, status code, reason phrase, redirect target, duration, selected headers, payload sample metadata, and extracted page metadata such as title, description, canonical, robots, Open Graph, Twitter, and meta refresh values.

## Errors

Empty URL, invalid URL, unsupported scheme, embedded credentials, unsupported port, DNS resolution failure, private or reserved network target, request failure, invalid Location header, or redirect loop. Reaching max_hops returns a warning with the partial chain.

## Auth And Limits

Anonymous JSON API for initial rollout. Use the /api/v1 endpoint for agents; browser form submissions remain protected by CSRF and reCAPTCHA.

JSON API uses the standard API throttle. Each request may perform up to max_hops outbound HTTP requests, so agents should keep max_hops low unless a longer chain is expected.

## Examples

### Requests

```text
GET /api/v1/redirect-chain?url=https://bit.ly/example
```

```text
POST /api/v1/link-expander {"url":"https://example.com","max_hops":5}
```

### Responses

```json
{"skill":"redirectchain","normalized_url":"https://short.example/abc","final_url":"https://example.com/landing","redirect_count":1,"chain":[{"hop":1,"status_code":301,"redirect_to":"https://example.com/landing"},{"hop":2,"status_code":200,"metadata":{"title":"Example landing page"}}]}
```

## FAQ

### Is this the same as Is This a Redirect?

No. Is This a Redirect checks a DNS-backed DomainSure listing for redirect and shortener domains. Redirect Chain performs a live HTTP fetch and follows the actual Location headers.

### Does it return entire page bodies?

No. The response includes bounded payload samples, byte counts, hashes, and metadata so agents can inspect the chain without pulling unbounded bodies into the response.

### What targets are blocked?

The skill only fetches http and https URLs on standard ports and blocks targets that resolve to private or reserved network addresses.

## Related Skills

- [Is This a Redirect?](https://dnsskills.md/skills/is-this-a-redirect.md)
- [DNS Twister](https://dnsskills.md/skills/dns-twister.md)
- [Is This a Homoglyph?](https://dnsskills.md/skills/is-this-a-homoglyph.md)
