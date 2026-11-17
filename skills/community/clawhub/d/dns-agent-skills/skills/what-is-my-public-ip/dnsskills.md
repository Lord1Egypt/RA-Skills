<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# What Is My Public IP

Useful when a browser, script, agent, or remote workflow needs to know the public address it is using.

## Discovery

- Identifier: `whatismypublicip`
- Version: `v1`
- Category: Network identity
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/what-is-my-public-ip
- Agent Markdown: https://dnsskills.md/skills/what-is-my-public-ip.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/my-ip

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `GET https://app.domainhelp.com/api/v1/whatismypublicip`
  - Status: `live`
  - Response modes: `json`, `text`

## Input Contract

No input is required.

## Output Contract

Returns the caller IP address, observed_at timestamp, and request metadata useful for diagnostics.

## Errors

No domain-specific errors. Network-layer failures are returned by the HTTP client.

## Auth And Limits

Anonymous for initial rollout.

Public low-volume use. Formal headers and quotas are planned.

## Examples

### Requests

```text
GET /api/v1/whatismypublicip
```

### Responses

```json
{"ip":"203.0.113.10","skill":"whatismypublicip"}
```

## FAQ

### Does this return my private LAN address?

No. It returns the address observed by DomainHelp at the edge of the request.

## Related Skills

- [What Is My DNS Resolver](https://dnsskills.md/skills/what-is-my-resolver.md)
- [DNS Twister](https://dnsskills.md/skills/dns-twister.md)
