---
name: gdpr-data-export-tool
description: Build, audit, and operate Article 15 (right of access) and Article 20 (data portability) data export pipelines for GDPR, plus the equivalent CCPA/CPRA "right to know" and UK DPA 2018 SARs. Covers subject identification and authentication tiers (passkey, magic link, in-app re-auth, ID verification), data inventory across Postgres / MySQL / Elasticsearch / Mongo / S3 / Stripe / Intercom / Segment / Mixpanel / Snowflake / SaaS sub-processors, JSON+CSV+HTML packaging with a human-readable index, secure delivery (signed URL with 7-day expiry, password-protected zip, in-app download), 30-day SLA tracking and extension protocol, shared-record handling (third-party data minimization), audit logging for the controller's accountability obligation under Article 5(2), and Article 12 fee/refusal policy. Triggers on "gdpr export", "data subject access request", "dsar", "right of access", "article 15", "article 20", "right to data portability", "ccpa data export", "cpra request", "subject access request", "personal data export", "data portability", "right to know", "privacy export pipeline".
metadata:
  tags: ["gdpr", "compliance", "privacy", "data-export", "dsar", "right-of-access", "article-15", "article-20", "ccpa", "cpra"]
---

# GDPR Data Export Tool

Design and operate a data subject export pipeline that satisfies Article 15 (right of access), Article 20 (data portability), CCPA/CPRA right-to-know, and UK DPA SARs — without leaking other subjects' data, without missing the 30-day deadline, and without the legal team re-litigating each request. Acts as a senior privacy engineer who has shipped DSAR systems for B2C, B2B, fintech, and health-adjacent products.

## Usage

Invoke when implementing a DSAR system, auditing an existing one, responding to a regulator inquiry, or onboarding a new sub-processor that holds subject data. Equally useful for greenfield ("we need GDPR exports for our new SaaS") and remediation ("we got a regulator letter asking how our exports work").

**Basic invocation:**
> Design our Article 15 export flow end-to-end
> Audit our existing DSAR pipeline against GDPR
> Build a data inventory for our subject access requests

**With context:**
> Here's our schema and our SaaS vendor list — produce the inventory + export pipeline
> We got an Article 15 request that includes a shared chat thread — what data goes out?
> We're a processor for our customer; how do we route this DSAR?

The agent emits a data inventory worksheet, an authentication flow, the export pipeline architecture, packaging spec, audit log schema, ROPA-aligned vendor coordination plan, and an SLA tracker.

## Inputs Required

- **Role** — controller or processor (determines who the subject contacts and who exports)
- **Data stores** — every database, search index, object store, log store, analytics store, and SaaS holding subject data
- **Identity model** — how a subject is identified (email? user_id? phone? customer_id?)
- **Existing auth** — passkey, password, MFA, in-app session
- **Volume estimate** — DSARs per month (drives whether it can be human-handled or must be automated)
- **Sensitivity** — health, finance, kids, special categories under Article 9 raise the auth bar
- **Geography** — EU-only / UK-only / global determines which laws apply in parallel
- **Sub-processor list** — every vendor with a DPA who holds subject data

## Workflow

1. Confirm controller vs processor for each data flow (Article 28 contracts dictate routing)
2. Build the data inventory worksheet: every table, index, blob, vendor — column → data category → source → retention
3. Define subject identification: which identifiers map to which records, across stores
4. Define authentication tier per request type (Article 12 requires reasonable measures)
5. Design the export pipeline (worker + queue + storage); choose JSON/CSV/HTML packaging
6. Write the shared-data handler (when the subject's record references another subject)
7. Define delivery: signed URL with expiry, password from a separate channel, in-app download
8. Write the audit log schema: who requested, who authenticated them, what was exported, when, where to
9. Define SLA tracking: 30-day clock, extension to 60 or 90 days with notification, refusal policy
10. Wire vendor coordination: per-DPA endpoints to fetch subject data (Stripe, Intercom, Segment, etc.)
11. Document the Article 12 fee/refusal protocol for "manifestly unfounded" or "excessive" requests
12. Test with an internal subject (staff member) end-to-end before going live

## Article 15 vs Article 20 — Critical Differences

The two rights are commonly conflated. They are not the same and the export must respect both.

| Aspect | Article 15 (Right of Access) | Article 20 (Right to Portability) |
|--------|------------------------------|------------------------------------|
| **What's covered** | All personal data the controller holds about the subject | Only data the subject *provided* to the controller |
| **Format** | Any intelligible format; copy of personal data | "Structured, commonly used, machine-readable" — JSON/CSV/XML |
| **Derived data** | Included (analytics, scores, inferred attributes) | NOT included |
| **Server logs** | Included if they identify the subject | Not portability-eligible |
| **Lawful basis required** | Always available | Only if processing is by consent or contract |
| **Right to direct transfer** | No | Yes — controller-to-controller where feasible |
| **Information about processing** | Must be provided (purposes, recipients, retention, source) | Not required (portability is data-focused, not process-focused) |
| **Format constraint** | Readable to a layperson is fine | Must be reusable by another service |

**Practical rule:** Always answer both rights with one export by default. The Article 20 layer is a subset of the Article 15 export. Tag each record with which right covers it.

## Data Inventory Worksheet

The single most important artifact. Build this *before* writing pipeline code. Every team and every vendor must contribute a row.

```
| Store              | Object/Table       | Subject identifier  | Data categories          | Source     | Article 15 | Article 20 | Retention | Owner       |
|--------------------|--------------------|---------------------|--------------------------|------------|------------|------------|-----------|-------------|
| Postgres / users   | users              | id, email           | name, email, country     | direct     | Y          | Y          | indef     | platform    |
| Postgres / orders  | orders             | user_id             | order history, amounts   | direct     | Y          | Y          | 7y (tax)  | payments    |
| Postgres / orders  | order_items        | order.user_id       | items purchased          | direct     | Y          | Y          | 7y        | payments    |
| Postgres / risk    | risk_scores        | user_id             | fraud score, ML inferred | derived    | Y          | N          | 2y        | risk        |
| Elasticsearch      | search_logs        | user_id             | search queries           | direct     | Y          | Y          | 90d       | search      |
| S3 / uploads       | uploads/<uid>/*    | path prefix         | user-uploaded files      | direct     | Y          | Y          | indef     | platform    |
| S3 / logs          | app-logs/*         | user_id in payload  | request logs             | direct     | Y          | N          | 30d       | sre         |
| Stripe (vendor)    | customer.id        | metadata.user_id    | payment methods, charges | mixed      | Y          | partial    | per Stripe| payments    |
| Intercom (vendor)  | user.id            | metadata.user_id    | support conversations    | direct     | Y          | Y          | 5y        | support     |
| Segment (vendor)   | userId             | userId              | event stream             | direct     | Y          | Y          | 1y        | analytics   |
| Mixpanel (vendor)  | distinct_id        | distinct_id         | product analytics events | direct     | Y          | Y          | 5y        | analytics   |
| Snowflake / dwh    | analytics.users    | user_id             | aggregated, derived      | derived    | Y          | N          | indef     | data        |
| Marketing / Mailchimp | list members    | email               | newsletter subscription  | direct     | Y          | Y          | until unsub| marketing  |
| Backups            | nightly snapshots  | implicit            | snapshot of all of above | n/a        | N (excl)   | N          | 35d       | sre         |
```

**Inventory rules:**
- Every store with PII must have a row — including backups (which are typically excluded from export per recital 67 but must be documented as excluded).
- "Subject identifier" is the join key. Without one, you cannot find the subject's records.
- "Source" = direct (subject provided), derived (you computed), observed (you logged), third-party (other source).
- Article 20 includes only `direct` and `observed-but-by-the-subject`. It excludes `derived` and `third-party`.
- "Owner" is the engineering team; export pipeline pings them when the schema changes.

The inventory must be re-validated quarterly. Schema drift is the #1 cause of incomplete exports.

## Subject Authentication Flow

Article 12(6) allows the controller to ask for "additional information necessary to confirm the identity of the data subject" — but you cannot make the bar so high that you frustrate the right.

**Three tiers, tied to data sensitivity:**

```
TIER 1 — Logged-in subject, low sensitivity
  Use when: the subject is in an active session, data is non-special-category
  Method: in-app re-auth (re-enter password or pass biometric prompt)
  Audit: session ID + re-auth timestamp logged

TIER 2 — Logged-out subject or moderate sensitivity
  Use when: subject has no session OR data includes financial / location / behavioral
  Method: email magic link to the email on file + passkey on device
  Audit: link issuance, click, device fingerprint, IP class

TIER 3 — Special category data (Article 9) or high-risk inference
  Use when: health, biometrics, sex life, political opinions, religion, union membership, sexual orientation
  Method: government ID document verification (vendor: Onfido, Persona, Stripe Identity)
                + email magic link + passkey
                + 24-hour cooling-off before fulfilment (with right to cancel)
  Audit: verification result, document type, full chain
```

**Don't:**
- Require ID verification for low-sensitivity export (regulator will treat as obstruction)
- Accept claims like "I forgot my email, send to a new address" without ID + reset flow
- Use a phone OTP as the only factor — SIM swap is a documented attack on DSARs
- Charge a fee at this stage — Article 12(5) prohibits fees except for "manifestly unfounded or excessive" repeat requests

**For B2B / multi-tenant SaaS:** the *data subject* is the individual user, not the customer (employer). The customer (controller) is responsible for end-user DSARs in most cases — but if the SaaS is the controller for some data (e.g. account email for the user), the SaaS handles those bits directly.

## Export Pipeline Architecture

A single pattern works for almost everyone: **request → queue → fan-out workers → packager → secure delivery.**

```
[Subject portal] -- POST /dsar  -->  [API gateway]
                                          |
                                          v
                                   [Auth tier check]
                                          |
                                          v
                                   [DSAR table: NEW row, status=pending,
                                    deadline = now + 30d]
                                          |
                                          v
                                   [SQS / Cloudflare Queue / Pub/Sub]
                                          |
              -----------------------------------------------------------
              |             |             |              |              |
              v             v             v              v              v
        [pg-extractor] [es-extractor] [s3-extractor] [stripe-fetch] [intercom-fetch]
              |             |             |              |              |
              -----------------------------------------------------------
                                          |
                                          v
                                 [packager: JSON+CSV+HTML]
                                          |
                                          v
                                  [encrypt + zip + sign]
                                          |
                                          v
                              [signed URL + email link]
                                          |
                                          v
                                   [audit log entry]
```

**Implementation choices:**

- **Orchestration:** Temporal, AWS Step Functions, Inngest, or a plain DB-state-machine with retries. Use Temporal when fan-out exceeds 10 stores.
- **Queue:** SQS, GCP Pub/Sub, Cloudflare Queues, or RabbitMQ. Each extractor must be idempotent.
- **Worker isolation:** one extractor per store. Failures in one don't block others; partial export is acceptable with clear "missing" annotation.
- **Output staging:** write to a *DSAR-only* bucket (never the public/uploads bucket). Lifecycle policy: auto-delete 30 days after delivery.
- **Encryption:** zip with AES-256 password (random per export), or age-encrypted blob; password delivered out-of-band (SMS or in-app, not the same email as the link).
- **Time budget:** target 24-hour median fulfilment for routine requests; the 30-day SLA is the *outer* bound, not the design target.

## Packaging Format

A multi-format bundle satisfies both rights and survives non-technical subjects.

```
export-2026-04-12-uid-1234.zip
├── README.html          ← human-readable index, links to JSON/CSV
├── summary.json         ← { request_id, generated_at, subject_id, deadline, expiry }
├── identity/
│   ├── account.json
│   └── account.csv
├── orders/
│   ├── orders.json
│   ├── orders.csv
│   └── line_items.csv
├── communications/
│   ├── support_tickets.json
│   └── support_tickets.html
├── activity/
│   ├── login_history.csv
│   └── search_history.csv
├── files/               ← user-uploaded files in original format
│   ├── photo-001.jpg
│   └── document.pdf
├── derived/             ← Article 15 only, NOT Article 20
│   ├── risk_scores.json
│   └── README.txt       ← "These are derived attributes; not portable under Art 20"
├── processing-info/     ← Article 15(1)(a-h) requirements
│   ├── purposes.html
│   ├── recipients.html  ← list of sub-processors
│   ├── retention.html
│   ├── sources.html
│   └── rights.html      ← rectification, erasure, complaint to DPA
└── manifest.json        ← cryptographic hash of every file
```

**Per Article 15(1):** the export must also tell the subject:
- The purposes of processing
- The categories of personal data
- The recipients (especially third countries)
- The envisaged retention or criteria for it
- The rights they have (rectification, erasure, restriction, portability, complaint)
- The source if not collected from the subject
- The existence of automated decision-making (Article 22) and meaningful info about the logic

`processing-info/` covers all of this. Generate from the ROPA (record of processing activities); it should already exist as Article 30 documentation.

## Shared-Data Handling

The hardest part of any DSAR. Subject A requests their data; their data references Subject B (a chat partner, a co-worker, a beneficiary, a recipient).

**Rule (Article 15 recital 63):** the subject's right of access "should not adversely affect the rights or freedoms of others". You must minimise other subjects' data while still giving the requester their own.

**Patterns:**

| Scenario | Treatment |
|----------|-----------|
| Chat thread, B sent A messages | Include B's messages with B's identifier replaced by `B_<short-hash>`; redact B's email/phone if visible in payload. Include A's messages in full. |
| Order paid for B as gift recipient | Include the order; redact B's address to `<city>, <country>` precision; redact B's phone. |
| Shared workspace activity log | Include rows where A acted; for rows where B acted, drop them entirely (they are B's data, not A's). |
| Comment on a public post by B | Include A's comment; do not include B's full post body unless it's already public; reference by URL. |
| Customer support: A complained about B (employee) | Include the complaint as A's data; replace employee identifier with role descriptor ("Support Agent #4"). |
| ML training data containing A and others | Per Article 11, if controller cannot single out A, no Article 15 obligation; document this. If can: include only A's contributions. |

**Anti-pattern:** dumping the raw chat thread including B's messages with email visible. This breaches B's rights and creates a parallel breach for the controller.

When in doubt, redact and document the redaction in the manifest with a reason code (`R-OTHER-SUBJECT`, `R-CONFIDENTIALITY`, `R-IP-PROTECTION`). The subject can challenge the redaction with the DPA; the controller's documentation is the defence.

## Vendor / Sub-Processor Coordination

Article 28 requires sub-processors to assist the controller in fulfilling DSARs. Most major vendors expose APIs or self-serve portals; some require a ticket.

**Common vendors and their DSAR endpoints:**

| Vendor | Method | Latency |
|--------|--------|---------|
| **Stripe** | API: `GET /v1/customers/{id}` + `GET /v1/charges?customer={id}` + payment_methods. Stripe also supports a privacy portal request via dashboard. | Real-time |
| **Intercom** | API: `GET /users/{id}` + `GET /conversations?user_id={id}` | Real-time |
| **Segment** | Privacy API: POST `/v1/workspaces/{w}/regulations` (action=suppress_with_delete) for erasure; for access, export from Segment's privacy portal | 30 days |
| **Mixpanel** | Compliance API: POST `/api/2.0/data-deletions` (deletion); access via support ticket or compliance API export | 30 days |
| **Amplitude** | Privacy & compliance API; access via the privacy dashboard | 30 days |
| **Mailchimp** | API export per list member; webhook listener for updates | Real-time |
| **HubSpot** | API + GDPR compliance settings dashboard (full export) | 30 days |
| **Sentry** | API or support ticket; logs containing user IDs are scrubbed via the dashboard | 30 days |
| **Datadog** | Logs may contain PII — export via Datadog's GDPR portal, or use scrubbing rules to prevent ingestion | 30 days |
| **Zendesk** | API: list tickets by requester; account-level export available | Real-time |

**Coordination rules:**
- Maintain a vendor table mapping `(vendor, our_user_id) → vendor_user_id`. Without it, you can't query.
- For vendors with 30-day windows: kick off vendor request *first*, before the in-house extraction, to overlap timelines.
- Always include a "Sub-processors contacted" annotation in the export so the subject knows who held data.
- For erasure (Article 17), request deletion from each vendor; track with the vendor's confirmation ID.

**Inventory completeness check:** any vendor in your DPA register must have an inventory row. Marketing tools that "just send emails" still hold the email address.

## SLA Tracking and Article 12 Compliance

**The 30-day clock** starts when the request is received and identity is reasonably confirmed. Extension to 60 or 90 days is allowed under Article 12(3) for complex requests, but the subject must be *notified* of the extension within the original 30 days with reasons.

```
DSAR row state machine:
NEW                    -- subject submits, identity not yet confirmed
AUTHENTICATING         -- magic link / ID verification in flight
AUTHENTICATED          -- start the 30-day clock here
EXTRACTING             -- workers fanning out
PACKAGING              -- packager building the bundle
DELIVERED              -- signed URL sent
EXPIRED                -- 7-day download window passed
EXTENDED               -- 30-day extension declared and subject notified
REFUSED                -- manifestly unfounded/excessive (rare; document!)
WITHDRAWN              -- subject cancelled
```

**Refusal (Article 12(5)):** allowed only when "manifestly unfounded or excessive, in particular because of repetitive character." Even then, the controller must:
- Provide the reason in writing
- Inform the subject of their right to lodge a complaint with a DPA
- Inform of judicial remedies

A controller who refuses must be able to demonstrate the manifest unfounded-ness. Refusing one DSAR per year is acceptable; refusing 30 per year requires bulletproof documentation.

**Fees (Article 12(5)):** allowed only for excessive/repetitive or for additional copies. Calibrate to administrative cost; a "DSAR fee schedule" must be public if used.

## Audit Logging

Article 5(2) imposes the *accountability principle*: the controller must demonstrate compliance. Every DSAR action must be logged in a tamper-evident store.

```json
{
  "event_id": "uuid",
  "ts": "2026-04-12T08:31:00Z",
  "event_type": "dsar_received | auth_method_passed | auth_method_failed | extractor_started | extractor_completed | extractor_failed | packaged | delivered | downloaded | expired | extended | refused | withdrawn",
  "request_id": "dsar-2026-04-12-1234",
  "subject_id": "user-9876",
  "actor": "subject | system | privacy_team_user",
  "actor_id": "user-9876 | system | privacy@co",
  "auth_tier": 1 | 2 | 3,
  "metadata": { "extractor": "pg-orders", "rows_extracted": 4421, ... },
  "ip_class": "EU/eu-west-1",
  "redaction_reasons": ["R-OTHER-SUBJECT"]
}
```

Store in append-only log (CloudWatch Logs Insights, GCP Logging, or S3 with Object Lock). Retain at least 3 years per typical DPA expectations; align with your data retention policy.

## Common Scenarios

### "Subject claims they didn't get the email link"

The audit log shows `delivered` event with the link signed at T. Re-send a fresh link; never extend the original (signed URLs must remain time-bound). Investigate deliverability if pattern recurs (Mailgun reputation, SPF/DKIM).

### "Subject is a child (under 16 in most EU member states)"

Authority to make the request lies with the parent/guardian. Tier 3 auth + parental verification. Special category data may apply if health-related. Route through legal before fulfilment.

### "Employee leaves; they want their HR data"

If you are the employer (controller for HR), Article 15 applies normally. Carve out: legitimate-interest-protected investigations, ongoing performance reviews not yet shared, and confidential references from third parties (Article 15(4) — others' rights).

### "We're a B2B SaaS; the user's employer is the controller"

Route the request to the customer's privacy contact (in your DPA). Provide the customer with an admin export. Don't fulfil end-user requests directly unless your DPA explicitly assigns you that obligation. Document the routing in the audit log.

### "Subject requests Article 17 erasure with the export"

Two separate rights with overlapping flows. Process the export first (Article 15/20), then queue the erasure (Article 17). Most pipelines reuse the inventory and the workers — erasure is "extract and delete" instead of "extract and package".

### "Request includes data from before our retention window expired"

If the data has been deleted under retention policy, document that in the export under `processing-info/retention.html` with the deletion date. The subject is entitled to know it existed and was deleted on schedule.

## Anti-patterns

- **A "send to engineering" Slack channel as the DSAR system** — no audit log, no SLA, no consistency. Build the pipeline.
- **Single PDF export with all categories mixed** — fails Article 20 machine-readability. JSON + CSV is mandatory for portability.
- **Plain email of the export zip** — fails encryption-in-transit assumption; password-protect and deliver out-of-band.
- **No expiry on the download URL** — link leaks become breaches indefinitely.
- **Re-using the user's app password to encrypt the zip** — password compromise = data compromise; generate a fresh one per request.
- **Including raw server logs** — they often contain other subjects' data; either filter or exclude with explanation.
- **Ignoring backups** — recital 67 lets you exclude them, but you must say so in the export.
- **Treating CCPA as identical to GDPR** — overlapping but distinct: CCPA's "right to know" has a 12-month look-back default; GDPR has none. CCPA permits more identity verification; GDPR is stricter on minimising friction.
- **Skipping the ROPA reference** — Article 15(1)(a-h) info comes from the ROPA. If the ROPA is stale, the export will be wrong.
- **Charging a fee by default** — only for excessive/repetitive; document the trigger.
- **Auto-fulfilment without a human-in-the-loop for Tier 3** — special category data deserves a 24-hour cooling-off and a privacy-team review.

## Exit Criteria

A DSAR pipeline is production-ready when:

- The data inventory is complete, every store has an owner, and a quarterly review is on the calendar
- A test DSAR (internal staff member) round-trips end-to-end in under 24 hours
- Authentication tiers are documented and enforce sensitivity-appropriate methods
- The packager produces a multi-format bundle with a manifest and processing-info section
- Shared-data redactions follow documented rules with reason codes
- Vendor coordination is automated for vendors with APIs and ticketed for the rest
- The 30-day SLA tracker dashboards median, p95, breaches, and extensions
- Refusal protocol is written and signed off by legal
- Audit log is append-only and retained per policy
- Privacy team has runbooks for the common scenarios above
- A regulator-ready response template exists for "describe how you handle DSARs"
