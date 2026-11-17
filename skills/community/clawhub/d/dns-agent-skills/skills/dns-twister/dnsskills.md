<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# DNS Twister

Supports typo, phishing, bit-flip, and homoglyph-adjacent domain intelligence workflows.

## Discovery

- Identifier: `dnstwister`
- Version: `v1`
- Category: Domain intelligence
- Status: `live`
- Access: `open-basic`
- Human docs: https://dnsskills.md/skills/dns-twister
- Agent Markdown: https://dnsskills.md/skills/dns-twister.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/dns-twister

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

## Runtime And Timeout Guidance

- Mode: `blocking`
- Default mode: `generate-only-no-expanded-tlds`
- Expected runtime: 1-10 seconds
- Expected runtime with `resolve=true`: 30-75 seconds
- Recommended client timeout: 90 seconds
- Server timeout: 75 seconds
- Retry guidance: Do not retry while the original request is still open. If resolve=true times out, retry with resolve=false for fast variant generation or retry the deep scan later.
- Progress guidance: This initial endpoint does not stream progress. Default resolve=false requests skip DNS resolution and the expanded TLD dictionary. Requests return JSON 504 if they hit the server timeout.

- `POST https://app.domainhelp.com/api/v1/dns-twister`
  - Status: `live`
  - Response modes: `json`

## Input Contract

Provide a fully qualified ASCII domain name. Optional resolve boolean defaults to false for fast agent use. The default skips DNS resolution and the expanded TLD dictionary. Set resolve=true only when DNS observations and expanded TLD swaps are required. Optional timeout_seconds may be set from 5 to 75 seconds.

## Output Contract

Returns generated variants and variant type. When resolve=true, rows may include observed IP address, additional DNS information, and expanded TLD swaps. Timeout responses return timed_out=true with guidance.

## Errors

Invalid domain, backend generation process failure, or a 504 timeout if the server-side process limit is hit.

## Auth And Limits

Anonymous JSON API for initial rollout. Use the /api/v1 endpoint for agents; browser form submissions remain protected by CSRF and reCAPTCHA.

JSON API uses the standard API throttle. Default resolve=false calls are intended to be fast. Deep resolve=true calls are bounded by a server timeout.

## Examples

### Requests

```text
POST /api/v1/dns-twister {"domain":"example.com"}
```

```text
POST /api/v1/dns-twister {"domain":"example.com","resolve":true,"timeout_seconds":75}
```

### Responses

```json
{"domain":"example.com","resolve":false,"timed_out":false,"rows":[{"type":"homoglyph","domain":"example.com"}]}
```

## FAQ

### How is this different from the homoglyph skill?

DNS Twister generates possible lookalike domains for a target. The homoglyph skill analyzes a supplied string or domain.

### Can an agent post to the web form route?

No. Agents should post JSON to /api/v1/dns-twister. The /dns-twister/process route is a browser form path and intentionally requires CSRF and reCAPTCHA.

## Related Skills

- [Is This a Homoglyph?](https://dnsskills.md/skills/is-this-a-homoglyph.md)
- [Is This a Redirect?](https://dnsskills.md/skills/is-this-a-redirect.md)
- [Link Expander / Redirect Chain](https://dnsskills.md/skills/redirect-chain.md)
- [SPF Flattener](https://dnsskills.md/skills/spf-flattener.md)
