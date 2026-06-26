# A2WF Agent Implementer's Guide — Draft Recommendation

**Status:** Draft v1.0
**Date:** 2026-03-22
**Scope:** Concrete blueprint for the guide itself — structure, normative content, placement, and examples.

---

## 1. Purpose of the Guide

This guide exists to answer one question for agent/tool builders:

> **"My agent visits a website. How do I discover, parse, interpret, and comply with its `siteai.json` policy?"**

It is the **consumer-side companion** to the core specification. Where the spec defines the format, this guide defines correct **runtime behavior** for agents that encounter (or fail to find) a `siteai.json` file.

**Target readers:**
- Developers building AI agents or autonomous tools that browse/interact with websites
- Framework authors integrating A2WF support into agent SDKs or middleware
- QA engineers verifying agent compliance with site policies

**Non-goals:**
- Teaching website operators how to _author_ `siteai.json` (that belongs in a separate Publisher Guide)
- Defining the format itself (that is the core specification's job)

---

## 2. Exact Proposed Section Outline

```
1. Quick Start
   1.1  Minimal fetch-parse-check flow (10 lines, JS + Python)
   1.2  What your agent owes the website operator

2. Discovery
   2.1  Discovery order (normative, 4 steps)
   2.2  HTTP requirements per step (status codes, redirects, timeouts)
   2.3  Content-Type validation
   2.4  When no siteai.json exists — default posture
   2.5  Caching, TTL, and refresh strategy

3. Parsing
   3.1  JSON parse requirements (RFC 8259, UTF-8)
   3.2  Schema validation: when and how
   3.3  specVersion handling (known vs unknown versions)
   3.4  Unknown top-level keys: MUST ignore, MUST NOT reject
   3.5  Unknown permission keys within read/action/data: MUST ignore
   3.6  Malformed documents: fail-closed vs fail-open guidance

4. Permission Resolution
   4.1  Reading permission groups (read, action, data)
   4.2  Per-permission rule fields (allowed, rateLimit, humanVerification, note)
   4.3  Interpreting `allowed: false`
   4.4  Interpreting missing permission keys (implicit deny vs implicit ignore)
   4.5  Applying `defaults` as fallback values
   4.6  Rate limit enforcement model

5. Agent Identification
   5.1  User-Agent requirements
   5.2  Sending required fields
   5.3  Trusted vs blocked agent matching
   5.4  Behavior when `allowAnonymousAgents: false`

6. Human Verification
   6.1  Detecting that human verification is required
   6.2  Supported methods: redirect-to-browser, email-confirmation, sms-otp
   6.3  Agent behavior per method (hand off, pause, fail)
   6.4  Cross-referencing permissions.action.*.humanVerification
        with humanVerification.requiredFor
   6.5  What to do when method is unsupported by the agent

7. Scraping Policy
   7.1  Interpreting scraping booleans
   7.2  Relationship to permissions.read
   7.3  trainingDataUsage: implications for LLM pipelines

8. Legal and Compliance
   8.1  Reading legal.termsUrl — when to surface it
   8.2  EU AI Act fields: riskClassification, transparencyRequired
   8.3  Logging and auditability recommendations

9. Discovery Endpoints (discovery object)
   9.1  Using mcpEndpoint, a2aAgentCard, openApi
   9.2  Relationship to robots.txt and llms.txt

10. Caching, Refresh, and Expiry
   10.1  HTTP cache headers
   10.2  metadata.expiresAt
   10.3  Recommended polling interval
   10.4  Forced refresh scenarios

11. Error Handling Matrix
   11.1  Network errors during discovery
   11.2  Non-JSON response
   11.3  Valid JSON but schema invalid
   11.4  Unknown specVersion
   11.5  Partial document (missing REQUIRED fields)
   11.6  Decision table: continue / degrade / abort

12. Reference Implementations
   12.1  JavaScript (Node.js) — full discovery + parse + check module
   12.2  Python — full discovery + parse + check module
   12.3  Integration patterns (middleware, pre-request hook, SDK wrapper)

Appendix A: Permission Key Reference Table
Appendix B: Decision Flowchart (discovery → parse → resolve → act)
Appendix C: Glossary
```

---

## 3. GitHub vs Website Placement

### GitHub (canonical, normative)

| Artifact | Path |
|----------|------|
| Guide (markdown) | `docs/implementer-guide.md` |
| JS reference module | `examples/js/siteai-client.mjs` |
| Python reference module | `examples/python/siteai_client.py` |
| Decision flowchart (Mermaid) | embedded in guide |

The GitHub version is the **source of truth**. It uses RFC 2119 language and is versioned alongside the spec.

### Website (derived, accessible)

The website SHOULD mirror the guide with the following adjustments:

- **Dedicated page** at `a2wf.org/docs/implementer-guide/`
- Abbreviated Quick Start on the existing docs landing page
- Syntax-highlighted code examples (same source, rendered)
- Linkable section anchors for external references
- Omit appendices (link to GitHub instead)
- Add a "Last synced with spec commit: `<hash>`" notice

**Rule:** If the website version diverges from GitHub, GitHub wins.

---

## 4. Normative Behaviors the Guide MUST Specify

These are behaviors the guide must define with MUST/SHOULD/MAY language. Each maps to a testable assertion.

### Discovery

| ID | Behavior |
|----|----------|
| D-1 | Agent MUST attempt `/siteai.json` before any alternative method. |
| D-2 | Agent MUST follow HTTP redirects (301, 302, 307, 308) during discovery. |
| D-3 | Agent MUST validate `Content-Type: application/json` (or `application/json; charset=utf-8`). |
| D-4 | Agent SHOULD set a timeout of no more than 10 seconds per discovery step. |
| D-5 | Agent MUST NOT treat absence of `siteai.json` as blanket permission. |

### Parsing

| ID | Behavior |
|----|----------|
| P-1 | Agent MUST parse the document as UTF-8 JSON per RFC 8259. |
| P-2 | Agent MUST reject documents where `specVersion` is missing. |
| P-3 | Agent MUST ignore unknown top-level keys without error. |
| P-4 | Agent MUST ignore unknown permission keys within `read`, `action`, `data` without error. |
| P-5 | Agent SHOULD validate against the JSON Schema at `https://a2wf.org/schema/core-v1.0.json` when available. |
| P-6 | Agent MUST treat a JSON parse failure as "no valid policy found" and apply conservative defaults. |

### Permission Resolution

| ID | Behavior |
|----|----------|
| R-1 | A permission with `allowed: false` MUST be respected — the agent MUST NOT perform that action. |
| R-2 | A permission key that is absent from the document SHOULD be treated as "not explicitly allowed" (conservative interpretation). |
| R-3 | When `rateLimit` is specified, the agent MUST NOT exceed the stated requests-per-minute for that permission. |
| R-4 | When `humanVerification: true` on a permission, the agent MUST NOT complete the action autonomously. |
| R-5 | `defaults.maxRequestsPerMinute` applies as a ceiling when no per-permission `rateLimit` is set. |

### Agent Identification

| ID | Behavior |
|----|----------|
| A-1 | When `agentIdentification.requireUserAgent` is `true`, agent MUST send an identifying `User-Agent` header. |
| A-2 | When `allowAnonymousAgents` is `false`, agent MUST identify itself or abort the interaction. |
| A-3 | If the agent's identifier appears in `blockedAgents`, it MUST NOT proceed. |

### Human Verification

| ID | Behavior |
|----|----------|
| H-1 | When human verification is required and the method is `redirect-to-browser`, the agent MUST hand control to a human-operated browser. |
| H-2 | When the agent cannot fulfill any listed verification method, it MUST NOT proceed with the action. |
| H-3 | The agent MUST check BOTH `permissions.action.*.humanVerification` AND `humanVerification.requiredFor` — if either signals verification is needed, verification is needed. |

### Caching

| ID | Behavior |
|----|----------|
| C-1 | Agent SHOULD respect HTTP `Cache-Control` and `ETag` headers. |
| C-2 | Agent SHOULD re-fetch if `metadata.expiresAt` has passed. |
| C-3 | Agent SHOULD NOT cache a `siteai.json` for longer than 24 hours without re-validation. |

---

## 5. What NOT to Include Yet

| Topic | Reason |
|-------|--------|
| Publisher/authoring guide | Separate artifact (Step 04 generator spec covers the wizard) |
| CMS-specific instructions | WordPress/Shopify scaffolds exist separately |
| Conformance test suite details | That is Step 02 (conformance expansion plan) |
| Formal IETF/W3C process references | A2WF is not yet submitted to a standards body |
| Extension fields (`keySections`, `forms`, etc.) | The implementer guide covers core governance consumption only; extensions are descriptive, not behavioral |
| Multi-language negotiation protocol | Spec section 1.6 acknowledges this but defers detailed protocol |
| Agent-to-agent delegation of siteai.json | Out of scope for v1.0 |
| Enforcement mechanisms / penalty models | Out of scope; the guide covers compliant behavior, not policing |
| OAuth/API-key integration for trusted agents | Not defined in spec v1.0 |

---

## 6. Suggested File Path and Companion Files

```
spec/                              (existing repo root)
├── docs/
│   └── implementer-guide.md       ← PRIMARY ARTIFACT
├── examples/
│   ├── js/
│   │   ├── siteai-client.mjs      ← JS reference implementation
│   │   ├── siteai-client.test.mjs ← JS tests against fixtures
│   │   └── package.json
│   └── python/
│       ├── siteai_client.py       ← Python reference implementation
│       ├── test_siteai_client.py  ← Python tests against fixtures
│       └── requirements.txt
├── tests/
│   └── fixtures/                  (existing, reused by reference impls)
│       ├── valid/
│       └── invalid/
```

**New files total:** 7 (1 guide + 3 JS + 3 Python).
**Reused:** existing `tests/fixtures/` for both reference implementations.

---

## 7. Minimal JS Example Topics

Each example should be self-contained, runnable with Node.js 20+ and zero dependencies beyond `node:` builtins.

### Example 1: Discovery (`discover-siteai.mjs`)
```
- Attempt GET /siteai.json with 5s timeout
- On 404, parse robots.txt for SiteAI: directive
- On 404, fetch homepage HTML, extract <link rel="siteai">
- On 404, attempt /.well-known/siteai.json
- Return { url, document } or { url: null, document: null }
- Validate Content-Type header
```

### Example 2: Permission Check (`check-permission.mjs`)
```
- Given a parsed siteai document and a permission path (e.g., "action.checkout")
- Resolve: allowed, rateLimit, humanVerification
- Apply defaults fallback for rate limit
- Return { allowed: bool, rateLimit: number|null, humanVerificationRequired: bool }
```

### Example 3: Agent Identity Gate (`identity-gate.mjs`)
```
- Given agentIdentification config and agent's own metadata
- Check: is agent blocked? Is anonymous access allowed? Are required fields present?
- Return { proceed: bool, reason: string }
```

### Example 4: Pre-Request Middleware (`middleware.mjs`)
```
- Express/Hono-style middleware that an agent HTTP client can wrap
- Before each outbound request: discover → cache → check permission → enforce
- Demonstrates caching with TTL and ETag
```

---

## 8. Minimal Python Example Topics

Each example should be self-contained, runnable with Python 3.10+ and only `httpx` as an external dependency (stdlib otherwise).

### Example 1: Discovery (`discover_siteai.py`)
```
- Same 4-step discovery as JS
- Use httpx with timeout=5
- Parse robots.txt with stdlib
- Parse HTML <link> with html.parser (no BeautifulSoup dependency)
- Return dataclass: SiteAIResult(url, document, source_method)
```

### Example 2: Permission Check (`check_permission.py`)
```
- Function: check_permission(doc: dict, group: str, key: str) -> PermissionResult
- PermissionResult dataclass: allowed, rate_limit, human_verification_required
- Applies defaults fallback
- Raises on missing specVersion
```

### Example 3: Agent Identity Gate (`identity_gate.py`)
```
- Function: can_proceed(agent_id: AgentIdentity, config: dict) -> GateResult
- GateResult dataclass: proceed, reason
- Checks blocked list, anonymous policy, required fields
```

### Example 4: Async Discovery + Check (`async_client.py`)
```
- Full async flow: discover → validate → check permission → enforce rate limit
- Uses httpx.AsyncClient
- Token bucket rate limiter using asyncio
- Demonstrates integration into an async agent loop
```

---

## Implementation Notes

**Writing order recommendation:**
1. Write sections 2–6 first (Discovery through Human Verification) — these are the normative core
2. Write section 11 (Error Handling Matrix) — this forces clarity on edge cases
3. Write section 12 reference implementations against existing test fixtures
4. Write section 1 (Quick Start) last — extract from the reference implementations

**Review checkpoints:**
- After section 6: validate all normative IDs (D-1 through H-3) are covered
- After section 12: run reference implementations against `tests/fixtures/valid/` and `tests/fixtures/invalid/`
- Before merge: cross-reference every MUST/SHOULD/MAY against spec v1.0 wording

**Validator alignment:**
The existing semantic validator (`validator/index.js`) validates producer output. The implementer guide defines consumer behavior. These are complementary but distinct — the guide SHOULD reference the validator for "how to pre-check a document you fetched" but MUST NOT depend on it for runtime permission resolution.
