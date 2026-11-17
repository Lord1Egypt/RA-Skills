<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# Is This a Homoglyph?

Helps humans and agents decide whether a string or domain is an IDN, looks visually deceptive, and what it likely mimics.

## Discovery

- Identifier: `isconfusable`
- Version: `v1`
- Category: Internationalization and spoofing
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/is-this-a-homoglyph
- Agent Markdown: https://dnsskills.md/skills/is-this-a-homoglyph.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- Web UI: https://app.domainhelp.com/is-this-a-homoglyph

## Agent Invocation

Use the execution API endpoints below. Do not post to browser Web UI form routes; those routes are for humans and may require CSRF and reCAPTCHA.

- `GET/POST https://app.domainhelp.com/api/v1/isconfusable`
  - Status: `live`
  - Response modes: `json`

## Input Contract

Provide input or domain as a string up to 512 Unicode characters.

## Output Contract

Returns IDN status, input type, A-label, U-label, scripts detected, confusable class, likely mimics, character notes, risk level, and explanation.

## Errors

Empty input, invalid UTF-8, overly long input, or malformed punycode warning with fallback string analysis.

## Auth And Limits

Anonymous for initial rollout.

Public low-volume use. Formal headers and quotas are planned.

## Examples

### Requests

```text
{"input":"xn--ypal-43d9g.com"}
```

```text
GET /api/v1/isconfusable?input=xn--ypal-43d9g.com
```

### Responses

```json
{"is_idn":true,"is_confusable":true,"confusable_class":"mixed-script","likely_mimics":[{"string":"paypal.com"}]}
```

## FAQ

### Is this the same as punycode conversion?

No. Punycode conversion is included, but the skill also checks scripts, confusable characters, and likely visual mimic targets.

## Related Skills

- [DNS Twister](https://dnsskills.md/skills/dns-twister.md)
- [Is This a Redirect?](https://dnsskills.md/skills/is-this-a-redirect.md)
- [Link Expander / Redirect Chain](https://dnsskills.md/skills/redirect-chain.md)
- [What Is My DNS Resolver](https://dnsskills.md/skills/what-is-my-resolver.md)
