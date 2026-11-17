<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# SPF Flattener

Useful for mail operations, audits, and agent workflows that need to reason about SPF include expansion.

## Discovery

- Identifier: `spfflattener`
- Version: `v1`
- Category: DNS and email operations
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/spf-flattener
- Agent Markdown: https://dnsskills.md/skills/spf-flattener.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/spf-flatten

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `POST https://app.domainhelp.com/api/v1/spf-flattener`
  - Status: `live`
  - Response modes: `json`

## Input Contract

Provide a domain name whose TXT records contain an SPF policy.

## Output Contract

Returns traversal stages, raw output, final flattened SPF record, or a DNS/error message.

## Errors

Invalid domain, no SPF record, DNS lookup failure, flattening process failure.

## Auth And Limits

Anonymous JSON API for initial rollout. Use the /api/v1 endpoint for agents; browser form submissions remain protected by CSRF and reCAPTCHA.

JSON API uses the standard API throttle.

## Examples

### Requests

```text
POST /api/v1/spf-flattener {"domain":"example.com"}
```

### Responses

```json
{"domain":"example.com","finalSPFRecord":"v=spf1 ip4:192.0.2.0/24 ~all"}
```

## FAQ

### Should every SPF record be flattened?

No. Flattening can help with lookup limits, but it also creates maintenance obligations when provider ranges change.

### Can an agent post to the web form route?

No. Agents should post JSON to /api/v1/spf-flattener. The /spf-flatten/process route is a browser form path and intentionally requires CSRF and reCAPTCHA.

## Related Skills

- [DNS Twister](https://dnsskills.md/skills/dns-twister.md)
- [What Is My Public IP](https://dnsskills.md/skills/what-is-my-public-ip.md)
