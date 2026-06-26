---
name: code-documentation
description: >
  Comprehensive code documentation skill — use this any time documentation is requested, after
  any significant code change, when onboarding a new subsystem, auditing existing docs for accuracy,
  or when asked to "document", "update docs", "write docs", or "clean up comments". Covers three
  tightly coupled concerns: (1) inline file/function headers in source code, (2) subsystem-level
  .md docs, and (3) global architecture + API reference docs. Always apply this skill — do not
  improvise documentation standards. Also triggers for requests like "add comments", "document
  this file", "our docs are out of date", "generate API reference", or after a PR or feature branch
  is completed.
---

# Code Documentation Skill

## Purpose

This skill governs how code is documented at every level — from individual file headers to
global architecture docs. Apply it consistently across all projects. When in doubt: document
the *why*, not the *what*. The code already says what it does.

---

## Phase 0 — Before You Write Anything

1. **Scan the repo structure.** Understand what exists before touching anything.
2. **Identify subsystems.** Group files by domain (Auth, Billing, API Layer, etc.).
3. **Read existing docs first.** Check `/docs/` in both frontend and backend. Note what's
   present, missing, or stale.
4. **Confirm the active branch.** Never document against stale or wrong code.

---

## Phase 1 — Source File Standards

Apply to every file that is ≥ 20 lines OR is imported by other modules.

### 1.1 — Line 1: Full Path Comment

The very first line of every source file must be a comment containing the file's full path
from the project root. Use the comment syntax appropriate to the language.

```js
// src/services/auth/tokenService.js
```
```py
# src/services/auth/token_service.py
```

### 1.2 — File Header Block (lines 2–N)

Immediately after the path comment, add a header block. Use the language's block comment
syntax. This block is mandatory and must be kept accurate.

```
/**
 * File: src/services/auth/tokenService.js
 *
 * Overview:
 *   Issues, validates, and refreshes JWT tokens for authenticated sessions.
 *   Exists to centralise all token logic so Auth routes stay thin.
 *
 * Exports:
 *   - issueToken(userId, role) → signed JWT string
 *   - verifyToken(token) → decoded payload or throws
 *   - refreshToken(oldToken) → new signed JWT string
 *
 * Imported By:
 *   - src/routes/auth.js
 *   - src/middleware/requireAuth.js
 *
 * Imports:
 *   - jsonwebtoken  — signing/verification
 *   - config/env    — JWT_SECRET, TOKEN_TTL
 *
 * Notes:
 *   - Tokens expire in 15 min; refresh window is 7 days.
 *   - verifyToken throws on expiry — callers must handle.
 */
```

**Rules:**
- Keep it current. If you add an export, update Exports. If a new file imports this, update
  Imported By.
- Do not pad with boilerplate. Every line must be accurate and useful.

### 1.3 — Function Headers

Top of every non-trivial function (any function with logic beyond a single expression):

```js
/**
 * Signs a new JWT for the given user. Embeds userId and role in payload.
 * Throws if JWT_SECRET is not set in env.
 */
function issueToken(userId, role) { ... }
```

**Rules:**
- Max 2 sentences.
- Explain *why* the function exists or what makes it non-obvious, not just what it does.
- No parameter/return type breakdown unless the types are genuinely surprising.

### 1.4 — Inline Comment Rules

**Allowed (rare exceptions only):**
```js
const TIMEOUT = 5000 // 5 seconds
```

**Prohibited — remove on sight:**

| Pattern | Example | Why banned |
|---|---|---|
| Restating the code | `// enable proxy` above `proxy: true` | Zero information |
| Removed/old code notes | `// removed legacy handler` | Use git for history |
| Change log comments | `// changed to use v2 API` | Not a changelog |
| Section dividers | `// ---- helpers ----` | Use modules instead |
| Obvious steps | `// loop through users` above a users.forEach | Noise |

If you encounter these, **delete them**. They are clutter that erodes trust in real comments.

---

## Phase 2 — Subsystem Documentation

See `references/subsystem-doc.md` for the full template and field-by-field instructions.

**One `.md` file per subsystem, located at:**
- `/backend/docs/<subsystem>.md`
- `/frontend/docs/<subsystem>.md`

**Subsystem identification heuristics:**
- A cohesive domain handled by a directory or cluster of files
- Examples: `auth`, `billing`, `search`, `notifications`, `api-layer`, `data-layer`,
  `file-upload`, `websockets`, `admin`, `onboarding`

**Discovery checklist — identify a subsystem when you find:**
- [ ] A directory with 3+ related files
- [ ] A shared service/utility used by 3+ other files
- [ ] A distinct API surface (routes/controllers grouped by concern)
- [ ] A background job or scheduled process
- [ ] A third-party integration (Stripe, S3, Twilio, etc.)

**If a subsystem doc already exists:**
- Compare it against current code
- Remove anything describing code that no longer exists
- Add anything the doc misses
- Update all file maps, function names, and flow diagrams

---

## Phase 3 — Global Architecture Document

Location: `/docs/architecture.md` (or `/backend/docs/architecture.md` depending on repo layout)

See `references/architecture-doc.md` for the full template.

Required sections:
1. System Overview — what this product does in 2–3 sentences
2. Subsystems — bulleted list, one-liner per subsystem, link to its `.md`
3. High-Level Diagram — ASCII or Mermaid, showing subsystem relationships
4. Tech Stack — language, framework, DB, cache, queue, infra
5. Cross-Cutting Concerns — how auth, error handling, validation, config, logging, and
   testing work *across* the system (not per-subsystem)

---

## Phase 4 — API Reference

**Required if a backend exists.** Location: `/backend/docs/api.md`

For large backends: one file per subsystem, e.g. `/backend/docs/api-auth.md`,
`/backend/docs/api-billing.md`, then an index in `/backend/docs/api.md`.

See `references/api-reference.md` for the full endpoint template.

Every endpoint must document:
- Method + path
- Description (1 sentence — what this does for the caller)
- Request: path params, query params, body schema
- Response: success schema + status codes + error codes
- Source mapping: which controller file and service methods handle it

---

## Phase 5 — Validation Pass

After writing or updating docs, audit them:

```
## Documentation Audit

### Missing
- List any subsystem without a doc

### Outdated
- List any doc that references removed files, functions, or endpoints

### Incorrect
- List any wrong dependency, wrong export name, wrong flow description

### Recommendations
- Specific fixes with file locations
```

Do not skip this pass. Stale documentation is worse than none — it actively misleads.

---

## Enforcement Rules

These apply any time you touch code:

1. **Changed a function's logic?** → Update its header.
2. **Added or removed an export?** → Update the file header's Exports section.
3. **Added a new file that others import?** → Add the file header; update importers'
   "Imported By" lists if practical.
4. **Added or changed an API endpoint?** → Update `api.md`.
5. **Structural change to a subsystem?** → Update that subsystem's `.md`.
6. **Added a new subsystem?** → Create its `.md` from the template in
   `references/subsystem-doc.md`.
7. **Removed a file or feature?** → Find every doc that mentions it and remove those
   references.

**Never leave documentation in a state that describes code that doesn't exist.**

---

## Quick Reference: What Goes Where

| Concern | Location |
|---|---|
| File path + module summary | Top of every source file |
| Function purpose | Top of every non-trivial function |
| Subsystem deep-dive | `/[frontend\|backend]/docs/<name>.md` |
| System-wide architecture | `/docs/architecture.md` |
| API contracts | `/backend/docs/api.md` (or per-subsystem) |

---

## Reference Files

- `references/subsystem-doc.md` — Full subsystem doc template + instructions
- `references/architecture-doc.md` — Full architecture.md template
- `references/api-reference.md` — Full API endpoint documentation template
