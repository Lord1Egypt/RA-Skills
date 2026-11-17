# 📋 File-by-File Forensic Audit Pipeline (Tasks Template)

This file serves as a structured template to orchestrate a systematic, file-by-file `/forensic-audit` pipeline across your codebase.

> [!IMPORTANT]
> **Core Concept:** To prevent context bloat and ensure the deepest possible analysis of critical code paths, security rules, and database interfaces, the audit is split into individual file tasks. 
> 
> The main agent (orchestrator) coordinates the pipeline, spawning isolated subagents (with clean contexts) to inspect each file individually, logging the results, and finally merging them into a consolidated report.
>
> **Dual-Run for High-Risk Files:** For the highest-risk security/financial files (auth, payments, crypto/secrets), run the audit twice (`a`/`b`) with independent subagents (fresh context, no shared memory), then merge into `MERGED.md` — keeping the higher severity for shared findings and tagging unique ones `[Run A only]` / `[Run B only]`. Lower-risk infra/config files get a single pass.

---

## 🛠️ Execution Strategy & Rules (CRITICAL — read before starting)

### Phase 1: Parallel Auditing (Subagents)
- **Run in parallel:** Spawn and run ALL subagent tasks (`01a` through the last `b`-suffix task) concurrently in a single batch.
- **Subagent Role:** Each subagent operates in an isolated context, reads its target file(s), runs the `/forensic-audit` skill, and writes its `FINAL.md`.

### Phase 2: Pipelined Merging (Orchestrator — do NOT delegate)
- **Do not wait for all subagents:** As soon as both `runA` and `runB` for a dual-run scope are completed, the orchestrator must immediately merge them into `MERGED.md`.
- **Merge logically:** Combine shared findings (keep the higher severity of the two), and keep unique findings marked as `[Run A only]` or `[Run B only]`.
- **Do not delegate merges:** Merging requires comparing only two files — the orchestrator does this faster than spawning another subagent.

### Phase 3: Final Cross-Scope Merge (Orchestrator — do NOT delegate)
- **Deduplicate and group:** Once all individual reports and `MERGED.md` files are ready, the orchestrator reads them all, performs cross-scope deduplication, and compiles the master report (`AUDIT_FINAL.md`).
- **Include ALL findings:**
  - **CRITICAL & HIGH:** Each must include its file path, line number (`file:line`), and a detailed description with before/after diff.
  - **MEDIUM & LOW:** Group these as bulleted lists organized by scope. Do not omit any findings.
- **Cross-Scope Deduplication:** If the exact same issue pattern occurs across multiple files, combine them into a single `CRITICAL` or `HIGH` finding and list all affected files.
- **Sort by severity:** Order the consolidated findings strictly from `CRITICAL` ➔ `HIGH` ➔ `MEDIUM` ➔ `LOW`.
- **Do not delegate the final merge:** This requires full context of all scopes, which only the orchestrator possesses.

### Why the Orchestrator Handles Merges Directly
- **Merge (2 inputs):** The orchestrator processes this faster than spinning up a new subagent.
- **Final (N inputs):** Cross-file deduplication requires full context of all scopes — only the orchestrator has this.

### Progress & Context Rules
- **Progress Log:** After completing each task (subagent run or merge), append a line in `00_PROGRESS.md`:
  `[NN] | [File Path] | CRITICAL: X | HIGH: Y | MEDIUM: Z | DONE`
- **Context Preservation:** Do not output the entire contents of generated `FINAL.md` or `MERGED.md` reports into the chat context. Only confirm the generated file path and proceed to the next task to prevent token limit issues.
- **Directory Isolation:** Create a separate subfolder for each dual-run scope (e.g., `01_auth-routes/runA/`, `01_auth-routes/runB/`).
- **Prompt Template:** For each `runA`/`runB` task, instruct the subagent:
  `"/forensic-audit. File: [target file path]. READ-ONLY. Save FINAL to: [output path]. Focus: find security vulnerabilities, race conditions, and integrity issues in this file only. Severity: CRITICAL=exploitable / HIGH=likely vuln / MEDIUM=gap / LOW=hardening."`

---

## 🎯 Example Target Files

*Replace these placeholders with the critical security, database, and infrastructure files identified during your initial scan. Mark the highest-risk files (auth, payments, secrets/crypto) for dual-run.*

### Output Directory
`Output path: C:\Users\Username\Desktop\_Reports\audit_run32\`

### Checklist

- [ ] **01a_auth-routes** | Path: `src/routes/auth.ts` ➔ `01_auth-routes/runA/`
- [ ] **01b_auth-routes** | (Same file as 01a) ➔ `01_auth-routes/runB/`
- [ ] **01m_auth-routes-merge** | Merge 01a and 01b ➔ `01_auth-routes/MERGED.md`

- [ ] **02a_stripe-integration** | Path: `src/routes/stripe.ts` ➔ `02_stripe/runA/`
- [ ] **02b_stripe-integration** | (Same file as 02a) ➔ `02_stripe/runB/`
- [ ] **02m_stripe-integration-merge** | Merge 02a and 02b ➔ `02_stripe/MERGED.md`

- [ ] **03a_crypto-helper** | Path: `src/lib/crypto.ts` ➔ `03_crypto/runA/`
- [ ] **03b_crypto-helper** | (Same file as 03a) ➔ `03_crypto/runB/`
- [ ] **03m_crypto-helper-merge** | Merge 03a and 03b ➔ `03_crypto/MERGED.md`

- [ ] **04_session-routes** | Path: `src/routes/sessions.ts` ➔ `04_sessions.md`
- [ ] **05_sse-handler** | Path: `src/lib/sse-tickets.ts` ➔ `05_sse.md`
- [ ] **06_db-schema** | Path: `prisma/schema.prisma` ➔ `06_schema.md`
- [ ] **07_nginx-config** | Path: `nginx/nginx.conf` ➔ `07_nginx.md`
- [ ] **08_docker-compose** | Path: `docker-compose.prod.yml` ➔ `08_docker.md`

- [ ] **99_final-merge** | Merge all individual reports and `MERGED.md` files into `AUDIT_FINAL.md`
  Must include: severity rollup table, Top-5 CRITICAL/HIGH findings with `file:line`, cross-file deduplication.
