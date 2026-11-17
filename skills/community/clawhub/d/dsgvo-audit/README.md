# DSGVO/GDPR Compliance Audit Skill

<p align="center">
  <img src="images/logo.png" alt="DSGVO Compliance Audit Logo" width="200" />
</p>

A read-only, multi-phase audit protocol for AI coding assistants (Claude Code, Antigravity, and compatible agents). This skill systematically scans a codebase to identify regulatory and data privacy compliance gaps under the German DSGVO (GDPR), BDSG, and TTDSG.

Designed for automated and semi-automated workflows, this protocol focuses on detecting personal data exposure, missing legal bases, incomplete data subject rights implementation, and third-party data processor compliance gaps.

## Reference Stack & Architecture

While the skill is adaptable, its core rules and search patterns are optimized for a modern, multi-platform SaaS stack:

- **Frontend**: Next.js, React, or Vue (responsible for cookie banners, consent flows, Impressum, and Privacy Notices).
- **Backend/API**: Fastify, Express, or NestJS (responsible for processing logic, endpoints, logging, and background job scheduling).
- **Database**: Prisma ORM, PostgreSQL, or MySQL (defining data models, relations, cascades, and encryption at rest).
- **Desktop Clients**: Electron applications (caching local credentials, user configurations, and local PII storage).
- **Third-Party Integrations**: Stripe (payment processing), Twilio (VoIP, notification SMS/emails), and RustDesk (remote control features).

---

## The 7-Phase Audit Protocol

The audit protocol runs sequentially across seven distinct phases, each focusing on a specific regulatory requirement under the DSGVO:

### Phase 0: PII Inventory (Art. 4, 30 GDPR)
- **Database Schema Audit**: Scans database definitions (e.g., Prisma schemas) to build a registry of Personal Identifiable Information (PII) including names, emails, phone numbers, addresses, IP addresses, and device identifiers.
- **Sensitive Data Detection**: Identifies special categories of data (Art. 9 GDPR) and sensitive access credentials (such as RustDesk IDs and passwords).
- **Data Flow Mapping**: Traces the lifecycle of PII from system entry points, through internal APIs, to third-party integrations.
- **Log Leakage Audit**: Scans Fastify logs, error outputs, and Server-Sent Events (SSE) payloads for unintended PII logging.

### Phase 1: Legal Basis & Consent (Art. 6, 7, 9 GDPR)
- **Processing Legality**: Evaluates whether each category of processed PII is mapped to a valid legal basis (Art. 6(1)(a)-(f) GDPR).
- **Consent Collection (Art. 7)**: Audits consent banner implementations, consent storage immutability (to fulfill the burden of proof), and withdrawal mechanisms.
- **Special Category Exceptions (Art. 9)**: Audits explicit consent dialogs for high-risk operations (such as establishing remote system access).
- **Purpose Limitation (Art. 5(1)(b))**: Verifies that collected data is not reused for unauthorized secondary purposes.

### Phase 2: Data Subject Rights (Art. 15-22 GDPR)
- **Right of Access (Art. 15)**: Audits data export endpoints (e.g., `GET /api/dsgvo/export`) for full database coverage, IDOR protection, and secure retrieval limits.
- **Right to Erasure (Art. 17)**: Audits account deletion endpoints (e.g., `POST /api/dsgvo/delete-account`) to verify that all related user records, credentials, logs, and files are completely purged or anonymized, while respecting statutory retention exceptions.
- **Data Portability (Art. 20)**: Verifies that data subject exports are structured in machine-readable formats (JSON/CSV).
- **Rectification & Objection (Art. 16, 21)**: Audits endpoints allowing users to update their information or object to processing based on legitimate interests.
- **Deadline Compliance**: Evaluates workflows for processing incoming data subject requests within the 1-month statutory limit (Art. 12(3) GDPR).

### Phase 3: Data Minimization & Retention (Art. 5 GDPR)
- **Data Minimization (Art. 5(1)(c))**: Scans for redundant fields in data models that are collected but never utilized in application logic.
- **Storage Limitation (Art. 5(1)(e))**: Checks for automated data retention mechanisms (cron jobs or background workers) that delete or anonymize stale session logs, queue entries, and user history.
- **Anonymization Verification**: Evaluates whether deleted records are truly purged or if remaining fields permit re-identification.

### Phase 4: Third-Party Processors & Transfers (Art. 28, 44ff GDPR)
- **Stripe Compliance**: Checks webhook handling, DPA/AVV statuses, and US data transfer compliance under the EU-US Data Privacy Framework.
- **RustDesk Relays**: Evaluates whether remote control configurations rely on self-hosted servers or public relay servers, auditing data locations and the existence of DPAs.
- **Twilio SMS/VoIP**: Audits log retention for call records and messages, and verifies regional routing settings.
- **General Script Injections**: Identifies client-side tracking scripts (Google Analytics, Sentry) that may leak PII without proper user consent.

### Phase 5: Technical Security Measures (Art. 32 GDPR)
- **Encryption**: Verifies HTTPS enforcement, database connection TLS, and field-level encryption for sensitive credentials.
- **Access Control**: Audits authorization checks, ownership verification on API routes, and admin endpoint protection.
- **Breach Readiness**: Flags the presence or absence of basic procedural and technical anomaly-alerting mechanisms to meet the 72-hour regulatory notification limit (Art. 33 GDPR).

### Phase 6: DPIA, Impressum & DSE (Art. 13, 14, 35 GDPR; §5 DDG)
- **DPIA Threshold (Art. 35)**: Evaluates the system against EDPB WP248 criteria (vulnerable data subjects, systematic monitoring, large-scale processing) to determine if a Data Protection Impact Assessment is legally required.
- **Impressum Compliance (§5 DDG)**: Verifies the presence of all legally required corporate details, contact information, and registration IDs.
- **Datenschutzerklärung (Art. 13/14)**: Audits privacy notice pages for completeness (including DPO contact info, legal bases, processor list, data subject rights, and complaint pathways).

---

## Execution & Reporting Framework

The skill outlines a strict, evidence-based execution standard:

- **Strict Read-Only**: The agent must never modify or create files within the source code of the repository being audited. All outputs must be written to a designated `$outDir` (located outside the project source code).
- **Pre-Flight Scans**: Employs built-in `rg` (ripgrep) patterns to scan for PII, hardcoded secrets, SSE payloads, and missing endpoints before starting.
- **Metadata Headers**: Every report includes repo state details (Git HEAD hash, branch status, dirty files, and auditor roles) to ensure audit repeatability.
- **Standardized Findings**: Findings must cite precise file lines and detail the observed behavior, the relevant DSGVO article, the compliance gap, the regulatory risk, and clear remediation directions.
- **Severity Ratings**: Risk severity is rated based on regulatory fine potential under Art. 83 GDPR (Critical, High, Medium, Low, Note).

---

## Multi-Agent Pipeline & Orchestration

The repository includes [tasks-dsgvo-example.md](./tasks-dsgvo-example.md), which implements a dual-run pipeline using multiple autonomous subagents:

1. **Parallel Runs**: Runs two independent agents (Run A and Run B) in parallel for each of the 9 scopes of the codebase.
2. **Merge Pass**: The main orchestrator compares the reports and merges the findings to eliminate discrepancies.
3. **Challenge Pass**: Before generating the final report, the orchestrator performs a manual check against the actual code for all Critical and High findings to filter out false positives.
4. **Master Summary**: Generates a master rollup summary including a compliance score calculated using a weighted deduction model:
   $$\text{Score} = 100 - (\text{Critical} \times 20 + \text{High} \times 10 + \text{Medium} \times 5 + \text{Low} \times 1)$$

---

## Limitations

- **No Legal Advice**: Audit outputs represent technical and engineering evaluations of the codebase. They do not constitute formal legal counsel.
- **Static Analysis Limits**: Procedural compliance gaps (e.g., employee training records, written corporate policies) cannot be verified from source code alone.
- **Weighted Towards Reference Stack**: Search patterns are designed around the reference stack (Prisma, Fastify, Next.js, Stripe, Twilio, RustDesk) and should be updated if applied to other technology configurations.
