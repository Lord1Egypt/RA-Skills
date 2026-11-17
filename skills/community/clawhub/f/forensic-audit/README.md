<p align="center">
  <img src="images/logo.png" alt="Forensic Audit Logo" width="200" />
</p>

# Forensic Audit Skill

A three-phase, read-only forensic audit protocol for AI coding assistants (Claude Code, Antigravity, and compatible agents). Systematically searches a codebase for security vulnerabilities, race conditions, performance bottlenecks, and system resilience risks.

Developed against a Turborepo monorepo stack (Fastify, Prisma/PostgreSQL, Electron, Stripe, Twilio). Stack-specific sections are marked and can be adapted for other architectures.

## What It Does

Three sequential phases:

* **Phase 1: Security, Cryptography & Data Privacy**
  * Authentication & Authorization: privilege escalation, JWT expiry/refresh rotation (RTR), TOTP replay attacks.
  * IDOR validation: ownership checks on client-scoped endpoints.
  * Cryptography & Secret Hygiene: AES-256 key config, Electron `safeStorage`, hardcoded secrets, GDPR PII deletion/export.
  * Stripe Webhook Security: `stripe.webhooks.constructEvent` signature validation.

* **Phase 2: Database Integrity, Transactions & Performance**
  * Race conditions: TOCTOU races, atomic transactions for queue acceptance and voucher bookings.
  * Query Optimization: N+1 loops, missing indexes, unbounded queries.
  * Resource leaks: connection pool limits, SSE listener cleanup.

* **Phase 3: Architecture, SOLID, Resilience & Lifecycle**
  * Lifecycle & Timezones: DST-safe cron jobs, timezone-resilient scheduling.
  * SOLID & Error Handling: structured JSON error logs (no DB query leaks to client), fail-fast env var validation at startup.
  * Desktop Integration: Electron IPC bridge security (`contextIsolation`, `nodeIntegration`).

---

## How to Use

1. **Install:** Save `SKILL.md` into `~/.claude/skills/forensic-audit/SKILL.md`. Restart your agent session — the skill becomes available as `/forensic-audit`.
2. **Invoke with a defined scope:** One file or tightly-related file group at a time — e.g. `/forensic-audit on src/routes/auth.ts`. See Scope Discipline in SKILL.md — never point it at an entire repository in one pass.
3. **Read the report:** Each phase is written to a timestamped report in `%USERPROFILE%\Desktop\_Reports\<timestamp>\` (Windows) or `~/Desktop/_Reports/<timestamp>/` (Linux/macOS) — never inside the project repository.
4. **Auditing a whole codebase?** See the pipeline section below — generate a task list first, then run it one file at a time.

---

## Orchestrating a File-by-File Forensic Audit (Multi-Agent Pipeline)

For complex backend APIs, a single repository scan can miss subtle bugs (missing `await` before a DB transaction, a missing TOTP replay guard). The template in [tasks-forensic-example.md](./tasks-forensic-example.md) implements a file-by-file pipeline with dual-run for high-risk files.

1. Ask the agent to scan and generate a task list — identifying high-risk files (auth, payments, crypto) for dual-run.
2. Launch all `runA`/`runB` subagents concurrently in a single batch.
3. Merge each pair yourself as they complete (no subagent for merge).
4. Consolidate to `AUDIT_FINAL.md` with severity rollup and cross-file deduplication.

---

## Default Technology Stack

`SKILL.md` search patterns target:
* **Backend:** Fastify API, JWT plugin, TOTP verification, Server-Sent Events (SSE).
* **Database & ORM:** Prisma ORM, PostgreSQL.
* **Desktop Client:** Electron IPC bridges (`ipcMain`, `ipcRenderer`).
* **Integrations:** Stripe SDK, Twilio SDK.

## Custom Stack Adaptation

Replace Prisma/Fastify-specific patterns in `SKILL.md`:
1. **Search queries:** Update ORM method names (e.g. `prisma.findMany()` → Sequelize `.findAll()` or Django `.objects.all()`).
2. **Security rules:** Replace JWT/Stripe checkpoints with your stack's auth middleware and payment library.
3. **Transaction patterns:** Adjust to match Spring `@Transactional`, Django `transaction.atomic()`, etc.

## Known Limitations

- Findings are based on static code analysis — runtime behavior (actual race conditions under load, memory leaks in production) requires profiling, not audit.
- Stack-specific patterns (Prisma, Fastify, Electron, Stripe) may not match other architectures — adapt search patterns before running.
- Dual-run reduces false positives but does not eliminate them. Always verify `file:line` before treating a finding as confirmed.
- Security findings flagged here are surface-level. For penetration testing or formal security assessment, use a dedicated security expert.
- Severity ratings reflect likely exploitability in the reference stack context, not a formal CVSS score.
