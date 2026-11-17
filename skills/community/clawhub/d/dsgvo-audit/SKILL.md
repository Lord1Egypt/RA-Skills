---
name: dsgvo-audit
description: Multi-phase DSGVO/GDPR compliance audit skill and task list for agentic QA systems (Germany). Scans database schemas, controller files, auth, subject rights (export/erasure), log/stream leakage, and third-party processor integrations for GDPR/DSGVO compliance surface. Use when invoked as /dsgvo-audit, or asked for "DSGVO-Prüfung", "GDPR audit", "dsgvo check", or "compliance check".
---

# Skill: dsgvo-audit

## Trigger

Use this skill when the user invokes `/dsgvo-audit`, asks for:
- "DSGVO-Prüfung", "GDPR audit", "GDPR check", "compliance check"
- "GDPR violation check", "GDPR personal data flow"
- "account deletion check", "data subject rights check"
- "third-party processors", "Stripe AVV", "RustDesk DSGVO"

**Default behavior when invoked without a scope argument**: run the full 7-phase audit sequentially on the entire repository. When a scope is provided (e.g. `/dsgvo-audit Scope: auth-registration`), run only the phases relevant to that scope and note which phases were skipped.

**STRICT READ-ONLY**: Never modify, refactor, or create files inside the project repository. Only write reports to `$outDir` under `_Reports`.

For security/auth/crypto depth — use `forensic-audit`. For UX/product logic — use `product-ux-audit`. This skill focuses exclusively on DSGVO/GDPR compliance surface.

---

## Stack Context ([Project Name])

*Adaptation Tip: Replace the stack description below with your own target application components.*

Always carry this context through every phase — do not re-derive:

| Layer | Example Tech / Scope | DSGVO Relevance & Focus |
|-------|----------------------|-------------------------|
| Frontend | Next.js / React / Vue | Consent collection, cookies, privacy notice, Impressum |
| API / Backend | Fastify / Express / NestJS | Data processing, endpoints, backend validation, logs |
| Database | Prisma schema / PostgreSQL / MySQL | PII model definitions, cascades, retention, encryption |
| Desktop / Client apps | Electron / Native Clients | Local PII storage, credentials caching |
| Payment Gateway | Stripe / PayPal / Braintree | Art. 28 DPA (AVV), billing PII, webhook security |
| Communications | Twilio / SendGrid / Mailgun | SMS/Email sending, Art. 28, opt-out mechanisms |
| Event Streams | SSE / WebSockets / RabbitMQ | PII leakage in live message payloads |
| Background Workers | Cron jobs / BullMQ / Celery | Retention enforcement, automated deletion/anonymization |

---

## Execution Protocol

### Pre-flight (before any phase)

1. **Task list**: Create a TaskCreate entry for each phase. Mark each `in_progress` when starting, `completed` when the phase file is verified. Never mark a phase complete without file verification.

2. **Resolve output path**:

   Windows (PowerShell):
   ```powershell
   $outDir = "$env:USERPROFILE\Desktop\_Reports\dsgvo-audit_$(Get-Date -Format 'yyyy-MM-dd_HHmm')"
   New-Item -ItemType Directory -Force -Path $outDir
   ```
   Linux / macOS (bash):
   ```bash
   outDir="$HOME/Desktop/_Reports/dsgvo-audit_$(date +%Y-%m-%d_%H%M)"
   mkdir -p "$outDir"
   ```
   Abort if creation fails.

3. **Repo context** (embed in every report header):
   ```bash
   git rev-parse --short HEAD
   git branch --show-current
   git status --short
   ```

4. **PII Quick Scan** (run before Phase 0 to orient findings):
   ```bash
   # Personal data patterns in source
   rg -i "email|phone|telefon|name|address|adresse|geburtstag|birthdate|iban|kontonummer" \
     --type ts --type tsx -l

   # PII in console.log / app.log
   rg "console\.(log|error|warn)\(.*?(email|phone|name|token|password|rustdesk)" \
     --type ts -l

   # PII in SSE event payloads
   rg "reply\.raw\.write|res\.write|sendEvent" --type ts -l

   # Hardcoded PII or secrets in source
   rg -i "password\s*=\s*['\"][^'\"]{4,}|api_key\s*=\s*['\"]|secret\s*=\s*['\"]" \
     --type ts -l

   # Missing DSGVO endpoints
   rg "dsgvo|gdpr|delete-account|export|auskunft|loeschung" \
     --type ts -i -l

   # RustDesk credential storage
   rg "rustdesk|rdPassword|rdId|remoteId|accessCode" --type ts -l

   # Consent logging
   rg "consent|einwilligung|zustimmung|agreed|acceptedAt" --type ts -l

   # TODO/FIXME markers in DSGVO-adjacent code
   rg "TODO|FIXME|HACK" --type ts | rg -i "dsgvo|gdpr|delete|consent|privacy|datenschutz"
   ```

5. **Schema snapshot**:
   ```bash
   cat packages/db/prisma/schema.prisma
   # or:
   rg --files | rg "schema\.prisma"
   ```
   Read the full schema — it defines the PII surface.

---

### Report Header Template

```md
# [Phase Title]
**Date**: YYYY-MM-DD HH:MM
**Repo**: [repo root path]
**Git HEAD**: [short hash] ([branch])
**Dirty files**: [git status --short output or "clean"]
**Auditor role**: [role for this phase]
---
```

### Finding Format

```
[file:line] SEVERITY — short title

**Observed**: what the code actually does (cite file:line)
**DSGVO Article**: Art. XX — what it requires
**Gap**: what is missing or broken
**Risk**: concrete consequence (fine, complaint, data breach)
**Fix direction**: concrete next step (no full rewrites)
```

Severity: **CRITICAL** (Art. violation, fine risk > €20k) / **HIGH** (likely violation, complaint risk) / **MEDIUM** (gap, best-practice miss) / **LOW** (minor, documentation gap) / **NOTE**.

---

## Phase Discipline

- **Fresh pass per phase** — do not rely on prior-phase memory; re-read relevant files for each phase's specific lens.
- **Cross-phase dedup** — if a finding was already reported in a previous phase, write `→ see Phase N: [brief label]` instead of repeating the full finding. Ownership:
  - **Phase 0** owns PII inventory findings (what data exists, where it lives).
  - **Phase 1** owns legal basis findings (Art. 6/7/9 gaps).
  - **Phase 2** owns data subject rights findings (Art. 15-22 endpoint gaps).
  - **Phase 3** owns retention/minimization findings (Art. 5 storage limitation).
  - **Phase 4** owns third-party processor findings (Art. 28/44ff gaps).
  - **Phase 5** owns technical security findings (Art. 32 measures) — defer depth to `forensic-audit`.
  - **Phase 6** owns DPIA/Impressum/DSE findings.
  - If a finding fits multiple phases, record it fully in its owning phase and reference by `file:line` from the other.
- **Sequential phases** — Phase N+1 starts only after Phase N's deliverable is written and verified (> 500 bytes).
- **Verify write**: after each phase, confirm the deliverable file exists and contains at least one substantive finding. If a phase genuinely has zero findings, write an explicit "No findings — checked: [what was checked]" line.

---

## Phase 0 — PII Inventory

**Role**: EU Data Protection Officer.
**Task**: Create a complete map of what personal data the target project collects, where it lives, and under what legal basis.

### PASS 1: Prisma Schema PII Audit

Read `schema.prisma` (find via `rg --files | rg schema.prisma`). For every model, identify:
- Fields that are personal data (name, email, phone, address, IP, device ID, behavioral data)
- Fields that are special category data (Art. 9): health, biometric, location, access logs to private computers
- Whether each field has `@db.Text`, encryption marker, or is stored plaintext
- `onDelete` behavior — does cascade wipe PII or leave orphaned records?

**RustDesk-specific**: `rdId`, `rdPassword`, `accessCode`, or equivalent fields — these grant access to a private computer and qualify as **sensitive data** requiring heightened protection (Art. 9(1) analogy or at minimum Art. 32 strong encryption).

### PASS 2: Data Flow Map

For each PII category found in PASS 1, trace:
- Where it enters the system (registration form, operator input, API call)
- Which services/apps can read it (`apps/web`, `apps/api`, Electron apps)
- Whether it leaves the system (Stripe, Twilio, RustDesk relay server, external APIs)
- Where it is deleted (or not)

### PASS 3: Log & SSE PII Leakage

Check Fastify route files and SSE handler for PII appearing in:
- `console.log` / `app.log` / `fastify.log`
- SSE event payloads (`reply.raw.write(...)`)
- Error response bodies sent to client
- HTTP response headers

**Deliverable**: `$outDir\audit_0_pii-inventory.md`
**Verify write**: file must exist and be > 500 bytes before Phase 1 begins.

---

## Phase 1 — Legal Basis & Consent (Art. 6, 7, 9 DSGVO)

**Role**: EU DPO + DSGVO-Anwalt.
**Fresh pass** — re-read relevant files; do not rely on Phase 0 memory.

### PASS 1: Art. 6 Legal Basis per Processing Activity

For each PII category from Phase 0, determine which legal basis is claimed in practice:
- `lit. b` (Vertragserfüllung): processing necessary to deliver the service
- `lit. c` (rechtliche Verpflichtung): legal obligation (tax, commercial law)
- `lit. f` (berechtigtes Interesse): legitimate interest — is a balancing test documented?
- `lit. a` (Einwilligung): consent — see PASS 2

Check: is the legal basis actually documented anywhere in the codebase (comments, Datenschutzerklärung, database)? Or is it assumed?

### PASS 2: Consent Mechanism (Art. 7)

- Is consent collected before remote control sessions (RustDesk access)? Where is it logged?
- Is consent for marketing/tracking (if any analytics are present) collected with a proper consent banner (§25 TTDSG for cookies)?
- Check `apps/web` for: cookie banner, consent state storage, consent withdrawal mechanism.
- Is consent timestamp, IP, and text version stored immutably? (Nachweispflicht Art. 7(1))

### PASS 3: Special Category Data (Art. 9)

RustDesk grants access to a private computer — this may constitute processing of data revealing **private life** and requires a specific Art. 9(2) exception or at minimum an explicit consent (Art. 9(2)(a)).

Check whether:
- The privacy notice mentions this processing
- An explicit consent is obtained before first remote session
- The legal basis for storing RustDesk credentials is documented

### PASS 4: Purpose Limitation (Art. 5(1)(b))

Are data collected for one purpose used for another? Check:
- Does operator data (names, session logs) flow into analytics?
- Does client registration data get used for marketing without separate consent?

**Deliverable**: `$outDir\audit_1_legal-basis.md`
**Verify write**: > 500 bytes before Phase 2.

---

## Phase 2 — Data Subject Rights (Art. 15–22 DSGVO)

**Role**: EU DPO + QA Automation Lead.
**Fresh pass.**

For Germany: all requests must be fulfilled within **1 calendar month** (Art. 12(3)). Deadline runs from receipt. Extension to 3 months possible if complex — but user must be informed within month 1.

### PASS 1: Auskunftsrecht (Art. 15) — Right of Access

Find the data export/access endpoint (likely `GET /api/dsgvo/export` or similar):
- Does it return ALL personal data for the requesting user?
- Does it include: processed data, purposes, legal bases, retention periods, third-party recipients, source of data?
- Is it scoped to the requesting user only (no IDOR via user ID swap)?
- Is the download URL time-limited or user-scoped?

### PASS 2: Recht auf Löschung (Art. 17) — Right to Erasure

Find the account deletion endpoint (likely `POST /api/dsgvo/delete-account`):
- Does it cascade-delete or anonymize ALL PII in all related models?
- Check every Prisma model with a `userId`/`clientId` relation — does `onDelete: Cascade` or `onDelete: SetNull` apply, or is the delete manual?
- Are RustDesk credentials (rdId, rdPassword) wiped on deletion?
- Are session recordings, chat logs, appointment history deleted or anonymized?
- Is there a retention exception logged (Art. 17(3) — legal obligation to keep billing records 10 years)?

### PASS 3: Recht auf Berichtigung (Art. 16) — Rectification

- Is there an endpoint/flow for users to correct their personal data?
- Does it update all copies (Prisma DB + any caches)?

### PASS 4: Datenübertragbarkeit (Art. 20) — Data Portability

- Does the export (Art. 15) also serve as the portability export?
- Is data exported in a machine-readable format (JSON, CSV) — not just human-readable PDF?

### PASS 5: Widerspruchsrecht (Art. 21) — Right to Object

- If legitimate interest (Art. 6(1)(f)) is used as legal basis for any processing: is there an object/opt-out mechanism?
- Is there an unsubscribe/opt-out for any marketing communications (if Twilio is used for notifications)?

### PASS 6: Deadline Tracking

- Is there any mechanism to track incoming data subject requests and their 1-month deadlines?
- Or does this entirely rely on manual process? (Note: this is a compliance gap even if not a code issue)

**Deliverable**: `$outDir\audit_2_subject-rights.md`
**Verify write**: > 500 bytes before Phase 3.

---

## Phase 3 — Data Minimization & Retention (Art. 5 DSGVO)

**Role**: EU DPO + Principal DBA.
**Fresh pass.**

### PASS 1: Datensparsamkeit (Art. 5(1)(c)) — Data Minimization

- Are there fields in Prisma models that are collected but never used in the application logic?
- Are full addresses stored when only city/postal code is needed?
- Are precise timestamps stored everywhere or only where needed?
- Is the full RustDesk session content logged, or only metadata?

### PASS 2: Speicherbegrenzung (Art. 5(1)(e)) — Storage Limitation

- Is there a documented retention policy per data category?
- Are there cron jobs that enforce deletion after retention period?
  - Check `proactive-outreach.ts` and other cron files for any deletion logic
  - If none exists: HIGH finding
- Session logs, appointment history, queue entries — are they ever deleted automatically?
- Stripe payment records: 10-year HGB retention is legal, but other Stripe webhook data?

### PASS 3: Anonymization vs Deletion

When an account is "deleted", does the system:
- Truly delete PII (preferred), or
- Anonymize (replace with `[deleted]` / null / hash)?
If anonymization: is it complete? No re-identification risk from remaining fields?

**Deliverable**: `$outDir\audit_3_retention.md`
**Verify write**: > 500 bytes before Phase 4.

---

## Phase 4 — Third-Party Processors & Data Transfers (Art. 28, 44ff DSGVO)

**Role**: EU DPO + Contract Lawyer (DE).
**Fresh pass.**

### PASS 1: Stripe (Zahlungsdienstleister)

- Stripe processes payment card data and billing PII — **Auftragsverarbeiter** (Art. 28)
- Check: is a Data Processing Agreement (DPA/AVV) with Stripe in place? (Stripe provides a standard DPA — but does the target project/company accept it?)
- Does Stripe send webhook data that includes PII? Check webhook handler for what's logged.
- Stripe servers in USA → international transfer. Is the Stripe DPA + SCCs sufficient? (Current: Stripe has EU-US Data Privacy Framework adequacy)

### PASS 2: RustDesk (Fernzugriff)

This is the highest-risk processor:
- Is RustDesk self-hosted (then: no third-party transfer) or using RustDesk's public relay servers (then: data transfer, potentially outside EU)?
- Find RustDesk config in `apps/api` or `apps/desktop` — what relay/rendezvous server is configured?
- If public RustDesk relay: where are these servers located? Transfer to non-EU = need SCCs or adequacy decision.
- Is there an AVV with RustDesk GmbH or the relay operator?
- Screen content during remote sessions — is it logged/recorded? Where?

### PASS 3: Twilio (Kommunikation)

- Twilio processes phone numbers and message content — **Auftragsverarbeiter**
- Is Twilio's DPA accepted?
- Twilio servers: EU region configured or US default? Check Twilio client initialization for region config.
- SMS content: does it include PII (names, appointment details)?

### PASS 4: Other Third Parties

- Any analytics tools on `apps/web` (Google Analytics, Plausible, etc.)? Check `layout.tsx`, `_app.tsx`, script tags.
- Error monitoring (Sentry, etc.)? Does it send PII in error payloads?
- Email provider (SendGrid, SES, Postmark)? AVV in place?
- Hosting provider (Hetzner, as mentioned earlier) — AVV for server hosting?

**Deliverable**: `$outDir\audit_4_processors.md`
**Verify write**: > 500 bytes before Phase 5.

---

## Phase 5 — Technical Security Measures (Art. 32 DSGVO)

**Role**: EU DPO + Security Engineer.
**Fresh pass. NOT a full security audit — defer depth to `forensic-audit`. Focus on DSGVO Art. 32 minimum.**

### PASS 1: Verschlüsselung (Encryption at Rest & in Transit)

- RustDesk credentials (`rdId`, `rdPassword`) in database: encrypted or plaintext? Find the field and check for encryption helper usage.
- Client PII fields (name, address, phone): any field-level encryption, or rely solely on DB-level encryption?
- Is the database connection using TLS? (`DATABASE_URL` contains `sslmode=require`?)
- HTTPS enforced for all `apps/web` and `apps/api` endpoints?

### PASS 2: Zugriffskontrolle (Access Control)

- Can `apps/desktop` (client-facing) access other clients' data via API? Check ownership guards.
- Can operators see data of clients not assigned to them?
- Admin endpoints (`/api/admin/*`): role-checked, or any authenticated user can call them?

### PASS 3: Pseudonymisierung (Art. 32(1)(a))

- Are analytics/logging events pseudonymized (hashed user IDs, not raw email)?
- Queue entries visible in SSE: do they contain full client names, or only IDs?

### PASS 4: Verfügbarkeit und Belastbarkeit (Art. 32(1)(b)(c))

- Is there a documented backup strategy? (Code evidence: backup cron, DB dump scripts)
- Note: full DR planning is out of scope here — flag absence as MEDIUM/LOW.

### PASS 5: Verletzungsmeldung Readiness (Art. 33/34)

- If a data breach occurs: is there a process (even non-code) to notify BfDI/Landesdatenschutzbehörde within 72 hours?
- Check for any breach detection/alerting code (anomaly detection, failed access alerts)
- Note absence as MEDIUM — this is mostly procedural but should be flagged.

**Deliverable**: `$outDir\audit_5_technical-measures.md`
**Verify write**: > 500 bytes before Phase 6.

---

## Phase 6 — DPIA Threshold & Impressum/DSE Check

**Role**: EU DPO.
**Fresh pass.**

### PASS 1: DSFA-Schwellenwert (Art. 35 DSGVO) — DPIA Threshold

Check the target project against EDPB WP248 rev.01 criteria to determine if a DPIA is required (e.g. due to remote computer access, systematic monitoring, processing of sensitive/location data, or vulnerable data subjects like children or elderly):

| Criterion | Project Specifics | Triggered? |
|-----------|-------------------|-----------|
| Evaluation/scoring of persons | e.g. credit rating, performance evaluation | Check |
| Automated decision-making | e.g. automated routing, profiling | Check |
| Systematic monitoring | e.g. screen access, location tracking | Check |
| Sensitive/special category data | e.g. biometric data, medical data, access credentials | Check |
| Large scale | e.g. large volume of data subjects | Check |
| Matching/combining datasets | e.g. merging user behavior data | Check |
| Vulnerable subjects | e.g. children, patients, employees | Check |
| New technology | e.g. machine learning, advanced telemetry | Check |
| Transfer to third countries | e.g. data transfer outside EEA | Check |

If ≥ 2 criteria: DPIA is **mandatory**. Flag as CRITICAL if no DPIA exists.

### PASS 2: Impressum (§5 DDG / §5 TMG)

Check `apps/web` for Impressum page (likely `/impressum` route):
- Vollständiger Name / Firmenname
- Anschrift (kein Postfach)
- E-Mail-Adresse
- Handelsregisternummer (if GmbH/UG/AG)
- Umsatzsteuer-ID or Steuernummer
- Verantwortlicher für den Inhalt (§18(2) MStV)

### PASS 3: Datenschutzerklärung (Art. 13/14 DSGVO)

Check `apps/web` for Datenschutzerklärung page:
- Verantwortlicher mit vollständiger Adresse
- Datenschutzbeauftragter (if required: §38 BDSG — 20+ employees processing automatically)
- All processing activities listed with legal basis and purpose
- Third-party processors named (Stripe, Twilio, RustDesk)
- Data subject rights explained (Art. 15-21)
- Right to lodge complaint with supervisory authority (Aufsichtsbehörde for the Bundesland)
- Cookie notice (if any tracking cookies used)
- International transfers disclosed

**Deliverable**: `$outDir\audit_6_dpia-impressum.md`
**Verify write**: > 500 bytes before Final.

---

## Challenge Pass (before Final Deliverable)

Before writing the master summary, validate every CRITICAL and HIGH finding from all phases.

- If subagents are available: spawn one fresh subagent (no shared context, read-only) per batch of findings (5–10 findings per batch). Give it only the finding text + repo path — not your reasoning. Use this prompt template:

  > "You are a DSGVO compliance reviewer with no prior context. Read the file at [repo path] and locate [file:line]. Verify the following finding against the actual code. Answer for each finding: **Confirmed**, **Overstated** (suggest downgraded severity and reason), or **Not an issue** (drop, with reason). Do not guess — cite the actual line you read.
  > Finding: [paste full finding block]"

- If subagents are not available: re-read the cited `file:line` yourself with fresh eyes and apply the same three-way verdict.

Apply the verdicts (drop/downgrade/keep) before building the rollup table. Note in the master summary how many findings were dropped/downgraded and why — this is a signal of audit quality, not a failure.

---

## Final Deliverable

Write `$outDir\audit_master_summary.md`:

```md
# DSGVO Audit — Master Summary
**Date**: YYYY-MM-DD
**Project**: [Project Name]
**Git HEAD**: [hash] ([branch])

## Compliance Score
[N]/100 — calculated as: 100 minus (CRITICAL×20, HIGH×10, MEDIUM×5, LOW×1)

## Severity Rollup

| Phase                     | CRITICAL | HIGH | MEDIUM | LOW | NOTE |
|---------------------------|----------|------|--------|-----|------|
| 0 PII Inventory           |        N |    N |      N |   N |    N |
| 1 Legal Basis & Consent   |        N |    N |      N |   N |    N |
| 2 Data Subject Rights     |        N |    N |      N |   N |    N |
| 3 Retention               |        N |    N |      N |   N |    N |
| 4 Third-Party Processors  |        N |    N |      N |   N |    N |
| 5 Technical Measures      |        N |    N |      N |   N |    N |
| 6 DPIA / Impressum / DSE  |        N |    N |      N |   N |    N |
| TOTAL                     |        N |    N |      N |   N |    N |

## Top 5 Critical/High Findings
1. [file:line] CRITICAL — ...
2. ...

## Quick Wins (fixable in < 1 day)
- ...

## Structural Fixes (require planning)
- ...

## DPIA Required?
[YES/NO/UNCERTAIN — with rationale]

## Bußgeldrisiko (Art. 83 DSGVO)
[LOW / MEDIUM / HIGH — with rationale]
```

Then concatenate all phase files into:
`$outDir\FINAL_dsgvo-audit_$(Get-Date -Format 'yyyy-MM-dd_HHmm').md`

Order: master summary → phase 0 → 1 → 2 → 3 → 4 → 5 → 6. Separate with `---` and `# Phase N: [title]` headings.

---

## Completion Output (to chat)

```
DSGVO/GDPR Audit completed. Saved to: [outDir]

Files:
- audit_0_pii-inventory.md
- audit_1_legal-basis.md
- audit_2_subject-rights.md
- audit_3_retention.md
- audit_4_processors.md
- audit_5_technical-measures.md
- audit_6_dpia-impressum.md
- audit_master_summary.md
- FINAL_dsgvo-audit_[timestamp].md

Compliance Score: [N]/100
DPIA Required: [YES/NO/UNCERTAIN]
Regulatory Fine Risk: [LOW/MEDIUM/HIGH]
```

---

## Known Limitations

- **Legal currency**: all legal references are based on DSGVO/BDSG/TTDSG/DDG as in force at time of writing. Verify regulatory text currency before relying on findings for formal filings or legal advice.
- **Stack specificity**: RustDesk, Stripe, and Twilio sections reflect the reference stack (Prisma/Fastify/Next.js). Adapt processor names, field names, and route patterns for other architectures.
- **Procedural gaps**: compliance gaps that are procedural rather than code-observable (missing DPA contracts, absent DPIA documentation, staff training, breach response procedures) are flagged where code evidence is absent, but cannot be fully verified from source alone.
- **Severity = regulatory risk, not exploitability**: CRITICAL means high fine risk under Art. 83 DSGVO, not necessarily an exploitable vulnerability. For security depth, pair with `forensic-audit`.
- **False positives**: the PII Quick Scan uses grep patterns and will match field names that are not actually personal data (e.g. `name` in a product model). The Challenge Pass filters these before the final report — do not skip it.
- **No legal advice**: audit findings are engineering observations about compliance surface. They are not legal advice and do not constitute a formal DSGVO assessment.

---

## Constraints

- **READ-ONLY** on project source. Zero writes inside the repository.
- **Evidence-only**: every finding cites `file:line`. No speculation framed as fact.
- **Timestamped output**: never overwrite previous audit runs.
- **Sequential phases**: Phase N+1 starts only after Phase N file is confirmed written and > 500 bytes.
- **TaskCreate/TaskUpdate**: create a task per phase at start, mark `in_progress` when beginning, `completed` after file verification.
- **No overlap with forensic-audit**: if a security vulnerability surfaces (e.g. IDOR), note it with pointer "→ forensic-audit for depth" rather than full finding.
- **No overlap with product-ux-audit**: UX issues noted only if they directly cause a DSGVO gap (e.g. consent dialog not visible).
- **Germany-specific**: all legal references are DSGVO + BDSG + TTDSG/DDG + applicable Landesrecht. Not UK GDPR, not US privacy law.
- **Severity = regulatory risk**, not exploitability. CRITICAL = Art. 83(5) fine territory (up to €20M or 4% global turnover).
- **Permission Handling**: If you do not have permission to write directly to `%USERPROFILE%\Desktop\_Reports`, request it using `ask_permission` for `write_file` with the target path, or execute file write operations via the `run_command` tool in PowerShell.
