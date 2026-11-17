# DSGVO/GDPR Compliance Audit Task List — Template r1
Output dir: [Target Path]\dsgvo-audit_r1\

## Execution Strategy (CRITICAL — read before starting)

### Phase 1: Parallel Audit (18 subagents)
- Launch ALL 18 runA/runB tasks (01a-09b) **in parallel as a single batch**.
- Each subagent: reads its scope → writes `FINAL.md` with DSGVO/GDPR findings.

### Phase 2: Merge per scope (DO IT YOURSELF, without subagents)
- **Do not wait for all 18.** As soon as both runA + runB for a single scope are ready → immediately merge them into `MERGED.md` yourself.
- Merge logic: 2 `FINAL.md` → 1 `MERGED.md` (take highest severity, deduplicate, use tags `[Run A only]`/`[Run B only]`).

### Phase 3: Final cross-scope merge (DO IT YOURSELF)
- Once all 9 `MERGED.md` are ready → read them all yourself → compile `DSGVO_FINAL_r1.md`.
- **Include ALL findings.** CRITICAL + HIGH — each with `file:line`, DSGVO article, and description. MEDIUM + LOW — grouped by scope.
- Cross-scope deduplication: same pattern in multiple scopes → single entry listing all scopes.
- Sorting: CRITICAL → HIGH → MEDIUM → LOW.
- Add Compliance Score: `100 − (CRITICAL×20 + HIGH×10 + MEDIUM×5 + LOW×1)`.
- Add: DPIA required? YES/NO/UNCERTAIN + justification.

### Why no subagents for merge/final
- Merge (2 inputs): you can do this faster yourself.
- Final (9 inputs): cross-scope deduplication requires full context — which only you possess.

---

## Rules

- Prompt for each runA/runB task:
  "/dsgvo-audit. Scope: [scope name]. Component: [tag].
  Relevant files (read these first, then discover more via skill pre-flight if needed):
  [list of files]
  READ-ONLY. Save FINAL to: [output path]
  Focus: find DSGVO/BDSG violations and risks only in this scope.
  Severity: CRITICAL=Art.83(5) fine risk / HIGH=likely violation / MEDIUM=gap / LOW=doc gap."

- Tasks 01a-09b are two independent runs of the same scope, each by a separate subagent with no shared context.

- Tasks with the suffix "merge" — DO NOT delegate to a subagent. Do it yourself:
  read both FINAL.md files → consolidate into MERGED.md
  (shared findings: severity = highest of the two; unique findings: tag with [Run A only]/[Run B only]).

- The final task (99) — DO NOT delegate to a subagent. Do it yourself:
  read all MERGED.md files → compile DSGVO_FINAL_r1.md.
  Include: Compliance Score, DPIA Decision, Fine Risk, Top-5 Critical/High, Quick Wins, Structural Fixes, and AVV Checklist.

- After each task, append a progress line to 00_PROGRESS.md:
  [NN] | [name] | CRITICAL:X HIGH:X MEDIUM:X LOW:X | DONE

- **Context Preservation:** DO NOT print the full content of FINAL.md / MERGED.md in the chat. Only confirm the file path and findings count, then proceed to the next task. This is critical to save the orchestrator's context window.

- **Directory Isolation:** Each scope should be a separate folder. Do not mix files from different scopes in the same directory.
  Structure: `dsgvo-audit_r1/[NN]_[scope-name]/runA/`, `runB/`, `MERGED.md`.

- **Challenge Pass (before task 99):** Before the final merge, read all CRITICAL and HIGH findings from all MERGED.md files. For each finding, verify `file:line` in the actual code once more and apply a verdict: **Confirmed / Overstated (downgrade) / Drop**. Record how many findings were dropped/downgraded — this acts as an audit quality metric.

---

## Tasks

- [ ] 01a_database-schema | [DB/Schema Module] | [e.g. packages/db/prisma/schema.prisma, migrations/] → dsgvo-audit_r1\01_database-schema\runA\
- [ ] 01b_database-schema | (same scope as 01a) → dsgvo-audit_r1\01_database-schema\runB\
- [ ] 01m_database-schema-merge | merge 01a + 01b → dsgvo-audit_r1\01_database-schema\MERGED.md
  Focus: PII fields, onDelete cascades, special category data, retention fields, database encryption markers.

- [ ] 02a_auth-registration | [Auth/Registration Module] | [e.g. apps/web/src/app/(login|register), apps/api/src/routes/auth.ts] → dsgvo-audit_r1\02_auth-registration\runA\
- [ ] 02b_auth-registration | (same scope as 02a) → dsgvo-audit_r1\02_auth-registration\runB\
- [ ] 02m_auth-registration-merge | merge 02a + 02b → dsgvo-audit_r1\02_auth-registration\MERGED.md
  Focus: Art. 7 consent at signup, Art. 13 info at collection, data minimization in registration form, PII leakage in auth logs/responses.

- [ ] 03a_subject-rights-endpoints | [DSGVO Endpoints] | [e.g. apps/api/src/routes/dsgvo.ts, apps/api/src/routes/account.ts] → dsgvo-audit_r1\03_subject-rights-endpoints\runA\
- [ ] 03b_subject-rights-endpoints | (same scope as 03a) → dsgvo-audit_r1\03_subject-rights-endpoints\runB\
- [ ] 03m_subject-rights-endpoints-merge | merge 03a + 03b → dsgvo-audit_r1\03_subject-rights-endpoints\MERGED.md
  Focus: Art. 15 export completeness (all PII fields?), Art. 17 cascade delete (all models?), Art. 20 machine-readable format, IDOR on export/delete, 1-month deadline tracking.

- [ ] 04a_sensitive-telemetry-consent | [Telemetry / Access Module] | [e.g. apps/desktop/src/telemetry.ts, apps/api/src/routes/sessions.ts] → dsgvo-audit_r1\04_sensitive-telemetry-consent\runA\
- [ ] 04b_sensitive-telemetry-consent | (same scope as 04a) → dsgvo-audit_r1\04_sensitive-telemetry-consent\runB\
- [ ] 04m_sensitive-telemetry-consent-merge | merge 04a + 04b → dsgvo-audit_r1\04_sensitive-telemetry-consent\MERGED.md
  Focus: Art. 6/7 consent before remote session/telemetry, consent logging (timestamp+IP+version), credential storage encryption, relay/data transfer locations, Art. 35 DPIA triggers.

- [ ] 05a_payment-billing | [Billing Module] | [e.g. apps/api/src/routes/subscriptions.ts, apps/web/src/app/billing] → dsgvo-audit_r1\05_payment-billing\runA\
- [ ] 05b_payment-billing | (same scope as 05a) → dsgvo-audit_r1\05_payment-billing\runB\
- [ ] 05m_payment-billing-merge | merge 05a + 05b → dsgvo-audit_r1\05_payment-billing\MERGED.md
  Focus: Art. 28 AVV/DPA with payment processors (Stripe/PayPal), webhook signature verification, PII in webhook logs, EU data residency, international transfers.

- [ ] 06a_communication-services | [Comms Module] | [e.g. apps/api/src/routes/notifications.ts, twilio.ts] → dsgvo-audit_r1\06_communication-services\runA\
- [ ] 06b_communication-services | (same scope as 06a) → dsgvo-audit_r1\06_communication-services\runB\
- [ ] 06m_communication-services-merge | merge 06a + 06b → dsgvo-audit_r1\06_communication-services\MERGED.md
  Focus: Art. 28 AVV/DPA with communication providers (Twilio/SendGrid), region config, PII in notification content, contact details retention, opt-out/unsubscribe mechanisms (Art. 21).

- [ ] 07a_frontend-documents | [Frontend Docs / Legal] | [e.g. apps/web/src/app/(impressum|datenschutz|privacy)] → dsgvo-audit_r1\07_frontend-documents\runA\
- [ ] 07b_frontend-documents | (same scope as 07a) → dsgvo-audit_r1\07_frontend-documents\runB\
- [ ] 07m_frontend-documents-merge | merge 07a + 07b → dsgvo-audit_r1\07_frontend-documents\MERGED.md
  Focus: Impressum completeness (DDG §5), Datenschutzerklärung completeness (all processors listed?), cookie consent banners (TTDSG §25), external scripts, CSP headers.

- [ ] 08a_logs-event-streams | [Logging / Event Streams] | [e.g. apps/api/src/routes/queue-sse.ts, logger.ts] → dsgvo-audit_r1\08_logs-event-streams\runA\
- [ ] 08b_logs-event-streams | (same scope as 08a) → dsgvo-audit_r1\08_logs-event-streams\runB\
- [ ] 08m_logs-event-streams-merge | merge 08a + 08b → dsgvo-audit_r1\08_logs-event-streams\MERGED.md
  Focus: Art. 32 PII leakage in live event streams (payloads), console.log/app.log PII exposure, log retention policies, pseudonymization of analytics events.

- [ ] 09a_retention-cron-jobs | [Cron / Background Jobs] | [e.g. apps/api/src/cron/, background workers] → dsgvo-audit_r1\09_retention-cron-jobs\runA\
- [ ] 09b_retention-cron-jobs | (same scope as 09a) → dsgvo-audit_r1\09_retention-cron-jobs\runB\
- [ ] 09m_retention-cron-jobs-merge | merge 09a + 09b → dsgvo-audit_r1\09_retention-cron-jobs\MERGED.md
  Focus: Art. 5(1)(e) Speicherbegrenzung (Storage Limitation) — automated PII deletion/anonymization mechanisms, cron jobs, retention periods, tax/commercial legal retention compliance.

- [ ] 99_final-merge | consolidate all MERGED.md files → dsgvo-audit_r1\DSGVO_FINAL_r1.md
  Must include: Compliance Score (0-100), DPIA Required (YES/NO/UNCERTAIN), Fine Risk (LOW/MEDIUM/HIGH), Top-5 CRITICAL/HIGH findings, Quick Wins (<1 day), Structural fixes (>1 day), DPA/AVV checklist (Stripe/Twilio/Hosting — status per processor).
