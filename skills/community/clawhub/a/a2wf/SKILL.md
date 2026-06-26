---
name: a2wf
description: Validate, generate, and audit A2WF siteai.json files — the open standard for AI agent governance on websites. Use when working with siteai.json policies, checking website A2WF compliance, generating agent permission files, or auditing how a site controls AI agent behavior. TRIGGER "a2wf", "siteai.json", "agent governance", "website ai policy", "agent permissions", "a2wf validate", "a2wf generate", "a2wf audit"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://a2wf.org","requires":{"tools":["web_fetch","exec"]}}}
---

# A2WF — Agent-to-Web Framework

A2WF is an open standard that defines what AI agents can and cannot do on a website via a machine-readable `siteai.json` file at the site root. Think of it as a legally actionable robots.txt for AI agents.

- **Spec:** <https://a2wf.org/specification/>
- **GitHub:** <https://github.com/a2wf/spec>
- **Schema:** <https://a2wf.org/schema/core-v1.0.json>

## Commands

### 1. Validate — Check a siteai.json

Validate a `siteai.json` file against the A2WF v1.0 spec. The validator is local-only (no network requests).

```bash
# Validate a local file
node {baseDir}/scripts/validate.mjs /path/to/siteai.json

# Validate from stdin
echo '{"specVersion":"1.0",...}' | node {baseDir}/scripts/validate.mjs --stdin
```

**To validate a live website:** Use `web_fetch` to download `https://example.com/siteai.json`, save to a temp file, then validate it.

**Output:** errors (must fix), warnings (should fix), info (suggestions). Exit 0 = valid, exit 1 = invalid.

If the user pastes raw JSON instead of a file path, save it to a temp file first, then validate.

### 2. Generate — Create a siteai.json

Build a spec-compliant `siteai.json` interactively or from parameters.

```bash
node {baseDir}/scripts/generate.mjs \
  --domain "https://example.com" \
  --name "Example Store" \
  --language "en" \
  --category "e-commerce" \
  --jurisdiction "EU"
```

When used interactively (no flags), ask the user:
1. Domain and site name
2. Category (e-commerce, news, healthcare, banking, restaurant, saas, other)
3. Jurisdiction and applicable laws
4. For each permission group (read/action/data): which operations to allow/deny
5. Rate limits, agent identification requirements, scraping policy

Output is a complete, validated `siteai.json` ready to deploy at the site root.

### 3. Audit — Analyze a website's A2WF posture

```bash
node {baseDir}/scripts/validate.mjs https://example.com --audit
```

Performs:
- Discovery check: Does `/siteai.json` exist? Correct content-type?
- Schema validation against core v1.0
- Permission completeness: Are critical permissions (scraping, account creation, data access) explicitly set?
- Legal coverage: Are jurisdiction and applicable laws declared?
- Extension check: Are companion extensions present and valid?

Outputs a structured report with a compliance score (0–100).

## Quick Reference

### siteai.json structure (v1.0)

```json
{
  "specVersion": "1.0",
  "identity": {
    "domain": "https://example.com",
    "name": "Site Name",
    "inLanguage": "en",
    "jurisdiction": "EU",
    "applicableLaw": ["GDPR", "EU AI Act"]
  },
  "permissions": {
    "read":   { "productCatalog": {"allowed": true, "rateLimit": 60} },
    "action": { "createAccount":  {"allowed": false} },
    "data":   { "customerRecords": {"allowed": false} }
  }
}
```

### Permission groups

| Group | Controls | Key examples |
|-------|----------|-------------|
| `read` | What agents can read | productCatalog, pricing, reviews, faq, contactInfo |
| `action` | What agents can do | search, addToCart, checkout, createAccount, submitContactForm |
| `data` | What data agents can access | customerRecords, orderHistory, paymentInfo, employeeData |

### Category templates

Use `--category` with generate to start from a template: `ecommerce`, `banking`, `healthcare`, `news-media`, `restaurant`, `saas`.

## For agent developers

When browsing a website, check for `siteai.json` at the domain root before taking actions. Respect the declared permissions — violations are documented and legally actionable under the declared jurisdiction.

See the full Agent Implementer Guide: `{baseDir}/references/implementer-guide.md`
