<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# Is This a Redirect?

Looks up a domain under redirects.domainsure.zone and reports whether it is listed as a redirect or URL shortener, including TXT explanations when present.

## Discovery

- Identifier: `isredirect`
- Version: `v1`
- Category: Domain intelligence
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/is-this-a-redirect
- Agent Markdown: https://dnsskills.md/skills/is-this-a-redirect.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/is-this-a-redirect

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `GET/POST https://app.domainhelp.com/api/v1/isredirect`
  - Status: `live`
  - Response modes: `json`

## Input Contract

Provide a fully qualified domain name. Browser users may paste a URL; the hostname is extracted before lookup.

## Output Contract

Returns normalized domain, lookup name, listed status, redirect-or-shortener boolean, A listing records, TXT explanations, verdict, and summary.

## Errors

Empty input, invalid domain, IP address input, overly long input, or DNS lookup failure.

## Auth And Limits

Anonymous JSON API for initial rollout. Use the /api/v1 endpoint for agents; browser form submissions remain protected by CSRF and reCAPTCHA.

JSON API uses the standard API throttle.

## Examples

### Requests

```text
GET /api/v1/isredirect?domain=bit.ly
```

```text
POST /api/v1/isredirect {"domain":"bit.ly"}
```

### Responses

```json
{"skill":"isredirect","domain":"bit.ly","lookup_domain":"bit.ly.redirects.domainsure.zone","is_redirect_or_url_shortener":true,"txt_records":["Known URL shortener."],"explanation":"Known URL shortener."}
```

## FAQ

### What DNS name is queried?

The skill queries the supplied domain below redirects.domainsure.zone, for example bit.ly.redirects.domainsure.zone.

### What does a TXT record mean?

When the lookup name has TXT records, the TXT text is returned as the explanation for the listing.

### Does not listed mean the domain never redirects?

No. It means the domain was not listed in this DomainSure redirect and URL shortener zone at lookup time.

## Related Skills

- [Link Expander / Redirect Chain](https://dnsskills.md/skills/redirect-chain.md)
- [DNS Twister](https://dnsskills.md/skills/dns-twister.md)
- [Is This a Homoglyph?](https://dnsskills.md/skills/is-this-a-homoglyph.md)
