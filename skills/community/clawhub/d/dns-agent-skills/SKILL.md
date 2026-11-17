<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# DomainHelp DNS Skills

Machine-readable catalog for DomainHelp DNS and domain utilities exposed as agent-ready skills.

- Human catalog: https://dnsskills.md/skills
- Markdown catalog: https://dnsskills.md/skills.md
- OpenAPI: https://dnsskills.md/openapi.yaml
- llms.txt: https://dnsskills.md/llms.txt
- Execution base: https://app.domainhelp.com

Use the documented `/api/v1/...` execution endpoints for agents. Browser Web UI form routes are intended for humans and may require CSRF and reCAPTCHA.

## Skills

### What Is My Public IP

Return the public IP address seen by DomainHelp.

- Identifier: `whatismypublicip`
- Version: `v1`
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/what-is-my-public-ip
- Agent Markdown: https://dnsskills.md/skills/what-is-my-public-ip.md
- Web UI: https://app.domainhelp.com/my-ip
- Endpoint: `GET https://app.domainhelp.com/api/v1/whatismypublicip`

### What Is My DNS Resolver

Detect the recursive DNS resolver in a request path.

- Identifier: `myresolver`
- Version: `v1`
- Status: `live-specialized-flow`
- Access: `open`
- Human docs: https://dnsskills.md/skills/what-is-my-resolver
- Agent Markdown: https://dnsskills.md/skills/what-is-my-resolver.md
- Web UI: https://app.domainhelp.com/my-resolver
- Endpoint: `POST https://app.domainhelp.com/api/v1/myresolver/check`
- Endpoint: `GET https://app.domainhelp.com/api/v1/myresolver/result`

### Is This a Homoglyph?

Analyze IDN, punycode, Unicode scripts, and visually confusable characters.

- Identifier: `isconfusable`
- Version: `v1`
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/is-this-a-homoglyph
- Agent Markdown: https://dnsskills.md/skills/is-this-a-homoglyph.md
- Web UI: https://app.domainhelp.com/is-this-a-homoglyph
- Endpoint: `GET/POST https://app.domainhelp.com/api/v1/isconfusable`

### Is This a Redirect?

Check whether a domain is listed as a redirect or URL shortener.

- Identifier: `isredirect`
- Version: `v1`
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/is-this-a-redirect
- Agent Markdown: https://dnsskills.md/skills/is-this-a-redirect.md
- Web UI: https://app.domainhelp.com/is-this-a-redirect
- Endpoint: `GET/POST https://app.domainhelp.com/api/v1/isredirect`

### Link Expander / Redirect Chain

Expand a URL and inspect every HTTP redirect hop.

- Identifier: `redirectchain`
- Version: `v1`
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/redirect-chain
- Agent Markdown: https://dnsskills.md/skills/redirect-chain.md
- Web UI: https://app.domainhelp.com/redirect-chain
- Endpoint: `GET/POST https://app.domainhelp.com/api/v1/redirect-chain`
- Endpoint: `GET/POST https://app.domainhelp.com/api/v1/link-expander`

### SPF Flattener

Resolve SPF includes and produce a flattened TXT record.

- Identifier: `spfflattener`
- Version: `v1`
- Status: `live`
- Access: `open`
- Human docs: https://dnsskills.md/skills/spf-flattener
- Agent Markdown: https://dnsskills.md/skills/spf-flattener.md
- Web UI: https://app.domainhelp.com/spf-flatten
- Endpoint: `POST https://app.domainhelp.com/api/v1/spf-flattener`

### DNS Twister

Generate and inspect lookalike domain permutations.

- Identifier: `dnstwister`
- Version: `v1`
- Status: `live`
- Access: `open-basic`
- Human docs: https://dnsskills.md/skills/dns-twister
- Agent Markdown: https://dnsskills.md/skills/dns-twister.md
- Web UI: https://app.domainhelp.com/dns-twister
- Runtime: mode `blocking`, default `generate-only-no-expanded-tlds`, expected 1-10 seconds, recommended client timeout 90 seconds, server timeout 75 seconds
- Endpoint: `POST https://app.domainhelp.com/api/v1/dns-twister`

## Mirror Repository

This repository mirrors the deployed DomainHelp DNS skill docs from https://dnsskills.md. Each skill is available locally at `skills/<slug>/dnsskills.md`.

- [What Is My Public IP](skills/what-is-my-public-ip/dnsskills.md)
- [What Is My DNS Resolver](skills/what-is-my-resolver/dnsskills.md)
- [Is This a Homoglyph?](skills/is-this-a-homoglyph/dnsskills.md)
- [Is This a Redirect?](skills/is-this-a-redirect/dnsskills.md)
- [Link Expander / Redirect Chain](skills/redirect-chain/dnsskills.md)
- [SPF Flattener](skills/spf-flattener/dnsskills.md)
- [DNS Twister](skills/dns-twister/dnsskills.md)
