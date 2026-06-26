# OpenClaw `domaininfo` Skill

A domain analysis skill that produces a domain-only report with:

- WHOIS summary
- DNS records (A/AAAA/NS/MX)
- Email security signals (DMARC/SPF/DKIM)
- TLS certificate info
- Optional website screenshot (only when screenshot tooling is already available)

## Usage

Type:

- `whois <domain>`

Supports:
- Plain domains (e.g., `example.com`)
- Full URLs (the skill extracts the domain)
- Emails (the skill extracts the domain after `@`)
- Internationalized domain names (IDNs) / non-ASCII domains (the skill can convert to Punycode automatically, e.g., `秒秒指南.com` → `xn--6krx87aehra.com`)

## Screenshot behavior (important)

Screenshot is an optional enhancement.

- If the runtime has OpenClaw browser automation available, the skill may capture a screenshot.
- If not, it must skip screenshot capture (no prompting the user to install Playwright/Chromium).
