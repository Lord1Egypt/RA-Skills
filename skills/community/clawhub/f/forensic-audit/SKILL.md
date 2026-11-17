---
name: forensic-audit
description: Three-phase read-only forensic audit of a codebase. Use when the user invokes `/forensic-audit`, asks to run a "forensic audit", "forensic audit pipeline", "multi-pass audit", "security audit", "vulnerability scan", "security check", or "code vulnerability scan".
---

# Skill: forensic-audit

## Trigger

Use this skill when the user invokes `/forensic-audit`, asks to run a "forensic audit", "forensic audit pipeline", "multi-pass audit", "security audit", "vulnerability scan", "security check", or "code vulnerability scan".

## Description

Three-phase read-only forensic audit of a codebase. Each phase is written to a timestamped report file before the next phase begins. Reports are saved to `%USERPROFILE%\Desktop\_Reports\<timestamp>\`.

**STRICT READ-ONLY**: Never modify, refactor, or create any files inside the project repository. Only write to the `_Reports` output folder.

---

## Execution Protocol

### Pre-flight (before any phase)

1. **Resolve output path**: `$outDir = "$env:USERPROFILE\Desktop\_Reports\$(Get-Date -Format 'yyyy-MM-dd_HHmm')"` — new timestamped subfolder every run to preserve previous audits.
2. **Create output dir**: `mkdir -p "$outDir"` (or equivalent PowerShell command) — confirm creation, abort if it fails.
3. **Capture repo context** (embed in every report header):
   - Current directory (repo root)
   - `git rev-parse --short HEAD` — git hash
   - `git branch --show-current` — branch name
   - `git status --short` — dirty/clean state
4. **Quick signal scan** (run before Phase 1 to orient findings):
   Use the `grep_search` tool (or `run_command` to run `rg`):
   ```bash
   # Unbounded queries
   rg "\.findMany\(\)" --type ts -l

   # Potential hardcoded secrets
   rg -i "password\s*=\s*['\"][^'\"]{4,}|api_key\s*=\s*['\"]|secret\s*=\s*['\"]" --type ts -l

   # Missing await / fire-and-forget risks
   rg "^\s*[^/].*\bprisma\." --type ts -l | head -20

   # console.log with sensitive-looking data
   rg "console\.(log|error)\(.*?(token|password|secret|hash)" --type ts -l

   # TODO / FIXME / HACK markers
   rg "TODO|FIXME|HACK|XXX" --type ts
   ```
5. **Directory snapshot**: `rg --files apps/api/src | sort` — full source tree before Phase 1.

---

### Report Header Template (prepend to every phase file)

```markdown
# [Phase Title]
**Date**: YYYY-MM-DD HH:MM
**Repo**: [repo root path]
**Git HEAD**: [short hash] ([branch])
**Dirty files**: [output of git status --short, or "clean"]
**Auditor role**: [role for this phase]
---
```

---

### Phase 1 — Security, Cryptography & Data Privacy

**Role**: Senior Cybersecurity Expert (OWASP), Cryptographer, EU DPO.

**Audit scope** — read the relevant source files using `view_file` or search via `grep_search`, then write findings:

#### PASS 1: Authentication & Privilege Escalation
- `POST /register`: guard preventing unauthenticated users from passing `role: "ADMIN"` or `role: "OPERATOR"` in the payload?
- JWT plugin: secrets verified against empty/default fallbacks? Expiration enforced? Refresh token rotation (RTR) atomic and replay-safe?
- TOTP `/totp/verify`: `lastUsedTotpCode` stored to prevent 30-second replay attacks?

#### PASS 2: Authorization & IDOR
- Every business route: explicit auth hook (`preHandler: [app.authenticate]`)? Unprotected endpoints?
- CLIENT-scoped endpoints (`GET /api/queue/:id`, `POST /api/appointments`, `POST /api/sessions/:id/feedback`): strict ownership validation, or IDOR via ID swap?

#### PASS 3: Rate Limiting & Brute Force
- `/login`, `/register`, `/forgot-password`, `/reset-password`, `/totp/verify`: is `rateLimit` config present? What are the limits? Are they adequate?
- Missing rate limit on any auth-adjacent endpoint = HIGH finding.

#### PASS 4: Cryptographic Practices & Secret Hygiene
- AES-256-GCM helper (`crypto.ts`): key length verified at startup? `authTag` and `iv` correctly stored/decrypted?
- Desktop credential storage: plaintext JSON in `%APPDATA%` or Electron `safeStorage`?
- `GET /clients` and similar: sensitive fields (encrypted passwords, raw tokens, hashes) explicitly excluded from Prisma `select`?
- Hardcoded secrets scan: any API keys, tokens, or passwords committed directly in source (`.ts`, `.js`, `.env.*` tracked by git)?
- `console.log` / `app.log` calls that print tokens, hashes, or raw PII?

#### PASS 5: Stripe Webhook Security
- `/webhooks/stripe`: webhook signature verified via `stripe.webhooks.constructEvent`? What happens if `STRIPE_WEBHOOK_SECRET` is missing?
- Is the raw body preserved (not parsed as JSON) before signature check?
- Does the handler log Stripe event payloads in a way that could expose customer PII?

#### PASS 6: GDPR / DSGVO Compliance
- Account deletion (`POST /api/dsgvo/delete-account`): cascade deletes/anonymizes orphaned `Client` PII (names, addresses, RustDesk access data)?
- Session consent handler: logs immutable metadata (IP, timestamp, clientId) confirming explicit consent before remote control?
- Data export (`GET /api/dsgvo/export`): does it include all personal data per Art. 20? Is the download URL scoped to the requesting user?

**Output format:**
```
## 1. Executive Summary (Security Focus)
## 2. Top Critical Security Vulnerabilities
## 3. Detailed Severity Breakdown

### CRITICAL findings
[file:line] CRITICAL — [problem]
\```diff
- before
+ after
\```

### HIGH findings
...

### MEDIUM findings
...

## 4. Severity Count
CRITICAL: N | HIGH: N | MEDIUM: N
```

Every finding: `[file:line] Severity — problem` + targeted before/after diff (≤30 lines context).
No full-file rewrites. No deletion of validation/`.refine()` blocks.

**Write result to**: `$outDir\audit_1_security.md`

**Verify write**: check file exists and size > 500 bytes. If empty or missing — do not proceed, report error.

---

### Phase 2 — Database Integrity, Transactions & Performance

**Role**: Principal DBA, Prisma ORM Expert, Performance Engineer.

Fresh file-system pass — re-read source files independently, do not rely on Phase 1 memory.

**Cross-phase dedup rule**: if a finding was already reported in `audit_1_security.md`, write `→ see Phase 1: [brief label]` instead of repeating the full diff.

#### PASS 1: Concurrency, Race Conditions & Isolation Levels
- Queue accept (`POST /api/queue/:id/accept`): atomic Prisma transaction preventing two operators from accepting the same client simultaneously?
- Voucher / appointment booking: `SERIALIZABLE` isolation with retry loop, or `READ COMMITTED` phantom-read risk?
- Any `findUnique` + conditional `update` pair outside a transaction (TOCTOU race)?

#### PASS 2: Prisma Optimization & N+1 Queries
- Admin metrics / dashboard (`GET /api/admin/metrics`, `GET /api/stats`): sequential loops or unbatched `Promise.all`? Consolidate to raw SQL or optimal `include`/`select`?
- Unbounded `findMany()` calls without `take`/`skip`/cursor — list every occurrence with file:line.
- `include` loading full relations when only a count or single field is needed?

#### PASS 3: Database Integrity & Indexes
- Compare queries in route files against `schema.prisma`: fields used in `where`/`orderBy`/joins — do they have `@@index` or `@unique`, or will they trigger full table scans?
- `onDelete` actions: `RESTRICT` blocking standard deletes, or accidental `CASCADE` wiping analytics logs?
- Missing unique constraints that should logically be unique (e.g., one active subscription per user)?

#### PASS 4: I/O, SSE & Connection Pooling
- SSE infrastructure (`queue-sse.ts`): `close` event removes listeners? Memory/socket leaks under reconnection storms?
- Prisma connection limit (`connection_limit` in `DATABASE_URL`) vs Fastify concurrent load?
- Long-running un-awaited promises that hold Prisma connections open?

**Output format:**
```
## 1. Database & Performance Summary
## 2. Concurrency & Race Condition Pitfalls
## 3. Query & Index Optimization Breakdown (with Diffs)

## 4. Severity Count
HIGH: N | MEDIUM: N | LOW: N
```

**Write result to**: `$outDir\audit_2_database.md`

**Verify write**: check file exists and size > 500 bytes. If empty or missing — do not proceed, report error.

---

### Phase 3 — Architecture, SOLID, Resilience & Lifecycle

**Role**: Senior Software Architect, SRE, QA Automation Lead.

Fresh file-system pass. Cross-phase dedup: if already in Phase 1 or 2 — reference it, don't repeat.

#### PASS 1: Logic, Timezones & Cron Lifecycles
- Background cron jobs (`proactive-outreach.ts`, `index.ts`): DST-safe? Europe/Berlin autumn/spring shifts handled without double-fire or skip?
- Schedule validation (`schedule.ts`): raw string comparisons (`"09:00" < "17:00"`)? Midnight crossovers? Night shifts (e.g., 22:00–06:00)?
- Batch cron loops: local `try/catch` per item, or one error aborts the entire batch for all remaining clients?

#### PASS 2: Architecture Purity & SOLID
- Route/controller files: direct DB + Stripe + Twilio calls without a service layer? List files where transport and business logic are mixed.
- Fastify plugins (Prisma, Stripe): wrapped in `fastify-plugin` (`fp`)? `onClose` lifecycle hooks registered?
- Single Responsibility: any one file doing >3 distinct concerns?

#### PASS 3: Infrastructure, Error Handling & Configuration
- Env-var wrappers (`mailer.ts`, `twilio.ts`): silent dry-run fallback in prod when var is missing, or safe startup crash?
- Error handlers: structured JSON logs, or raw stack traces / SQL query fragments exposed to client response?
- Missing startup validation: does the server fail fast with a clear message if `JWT_SECRET`, `DATABASE_URL`, or `STRIPE_SECRET_KEY` are absent?

#### PASS 4: Electron Lifecycle & Test Runner Isolation
- Desktop IPC bridges: arbitrary node module invocation possible via IPC? `before-quit` blocking synchronous network calls?
- `contextIsolation` and `nodeIntegration` settings in `BrowserWindow` config?
- Test suite: `app.inject()` in-process testing, or real `localhost` HTTP calls against a running server?
- Test mocks: any test that reaches a real DB, network, or filesystem without explicit opt-in?

**Output format:**
```
## 1. Architectural & Resilience Overview
## 2. Critical Lifecycle & Logic Issues
## 3. Structural Refactoring & Testability Breakdown (with Diffs)

## 4. Severity Count
HIGH: N | MEDIUM: N | LOW: N
```

**Write result to**: `$outDir\audit_3_architecture.md`

---

### Completion

After all three files are written and verified, output to chat:

```
Forensic audit completed. Saved to: [outDir]

Created files:
- audit_1_security.md
- audit_2_database.md
- audit_3_architecture.md
```

Then provide a **3-sentence executive summary** — one sentence per phase, each naming the single highest-severity finding and its file:line.

Finally, output a **combined severity table**:
```
| Phase       | CRITICAL | HIGH | MEDIUM | LOW |
|-------------|----------|------|--------|-----|
| Security    |        N |    N |      N |   N |
| Database    |        — |    N |      N |   N |
| Architecture|        — |    N |      N |   N |
| TOTAL       |        N |    N |      N |   N |
```

---

## Constraints (apply to all phases)

- **READ-ONLY on project source.** Zero writes, edits, or new git branches inside the repository.
- **Timestamped output** — never overwrite previous audit runs.
- **Report header required** — every file must start with date, git hash, branch, dirty state.
- **File write verification** — confirm each phase file is > 500 bytes before proceeding to the next phase.
- **No full-file rewrites** in reports. Diffs must be targeted (≤30 lines context).
- **No destructive fixes**: never suggest deleting validation or `.refine()` blocks. Fixes must extend business logic algorithmically.
- **Fault tolerance**: no top-level `throw Error` fixes that crash Electron / desktop clients. Always propose architectural fallbacks.
- **Cross-phase dedup**: Phase 2 and 3 must reference Phase 1 findings rather than duplicate them.
- **Sequential phases**: Phase N+1 starts only after Phase N file is confirmed written and non-empty.
- **Permission Handling**: If you do not have permission to write directly to `%USERPROFILE%\Desktop\_Reports`, request it using `ask_permission` for `write_file` with target `C:\Users\relig\Desktop` or execute the file write operations via the `run_command` tool in PowerShell.
