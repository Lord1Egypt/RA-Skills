---
name: domaininfo
license: MIT
description: "Look up domain WHOIS information, check email security (DMARC/SPF/DKIM), inspect TLS certificates, and capture website screenshots. Provides a comprehensive, domain-only report."
---

# domaininfo

Look up domain WHOIS information and (optionally) capture website screenshots.

## When to Use

When the user types `whois <domain>` or `whois <url>` or `whois <email>`:
- Strip any `https://`, `http://`, `www.` prefixes
- If input contains `@`, extract the domain part after `@` (e.g., `user@example.com` → `example.com`)

## Security Considerations

- **Input validation**: After extracting the domain, only allow alphanumeric, hyphen, and dot characters. Reject anything else.
- **Command injection prevention**: Never interpolate user input directly into shell strings. Prefer argument arrays / safe libraries.
- **Timeouts**: Every external call must have a bounded timeout (e.g., 10s for WHOIS/DNS, 10s for TLS).
- **Error handling**: On failure, return a generic user-friendly message and keep details internal.
- **Output sanitization**: Build the final message as a single string before sending; never send partial responses.
- **File-system safety**: If writing screenshots, restrict writes to a known directory under the skill folder and verify paths stay within it.
- **Rate-limiting & caching**: Cache IP-to-country lookups briefly to avoid hammering external services.

## Workflow (Strict Buffer-First — SAFE EXECUTION)

**CRITICAL**: Zero output until everything is ready. No progress messages.

### Phase 1 — Silent Buffer with Validation

1. **Extract & validate domain**
   - Strip `https://`, `http://`, `www.` prefixes.
   - If input contains `@`, take the part after `@`.
   - Validate with regex `^[a-z0-9.-]+$` (case-insensitive).
   - If invalid, abort and return “❌ Invalid domain”.
2. **WHOIS**: run `whois` via safe exec with timeout (10s). Store registrar data.
3. **DNS**: run `dig` for A, AAAA, NS, MX via safe exec with timeout (10s). Store results.
4. **IP Geolocation (Country Code)**
   - For each IP from A/AAAA and resolved NS/MX hostnames:
     - Query `https://ipinfo.io/{IP}/country` using `web_fetch` with timeout (5s).
     - Store the returned 2-letter country code.
5. **Email Security (DMARC/SPF/DKIM)**
   - DMARC: query TXT for `_dmarc.<domain>`
   - SPF: query TXT for `<domain>` and extract the string containing `v=spf1` (parse in code; avoid shell pipelines)
   - DKIM: query TXT for common selectors (`default`, `google`, `selector1`)

### Phase 2 — Optional Screenshot + TLS

#### Screenshot (ONLY if screenshot tooling is already available)

Only attempt a website screenshot if one of the following is already available in this runtime:

- **OpenClaw browser tool** (preferred): use the `browser` tool to navigate to the site and take a screenshot.
- **Bundled Playwright script**: `scripts/domain-screenshot.js` (only if Node + Playwright + a Chromium runtime are already installed).

If neither is available (missing tool / missing module / missing browser runtime), **skip the screenshot silently** and continue the report.

#### TLS/SSL Check (if HTTPS)

- Fetch certificate info with `openssl` (timeout 10s).
- Extract: certificate issuer and expiry date.
- If it fails or times out, note “TLS check failed” but continue.

### Phase 3 — Single Final Output

- If a screenshot was successfully captured, send it via the `message` tool.
- Send the final WHOIS + DNS + Email Security + TLS summary in **one** message only.

## Send Screenshot (SINGLE SEND ONLY)

Use `message` tool with action=send and filePath:

```json
{
  "action": "send",
  "caption": "domain.com screenshot",
  "filePath": "domain-screenshot.png"
}
```

Do NOT also implement provider-API fallbacks (e.g., raw HTTP requests). If message sending fails, report failure rather than double-sending.

## Setup Notes

- This skill does **not** include step-by-step installation instructions for Playwright/Chromium.
- Screenshot is an **optional enhancement** and must be skipped if screenshot tooling is not already present.
- See `references/setup.md` for non-invasive environment notes.
