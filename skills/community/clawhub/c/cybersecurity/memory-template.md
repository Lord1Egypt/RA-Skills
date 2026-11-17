# Working File Templates — Cybersecurity

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/cybersecurity/config.yaml` | Key by key, read-modify-write |
| Authorized scope, exclusions, allowed disruption, approval chain | `## Scope & Authorization` in `memory.md`; the long version at the path in `authorized_scope_file` | Rewritten in place; dated |
| Environment: crown jewels, systems, trust boundaries, log sources and their retention | `## Environment` in `memory.md`; `~/Clawic/data/cybersecurity/assets.md` past the split threshold | One entry per system or boundary |
| Open findings, and risks somebody accepted with an expiry date | `## Findings` in `memory.md`; `~/Clawic/data/cybersecurity/findings.md` past the threshold | One row per finding |
| Detection rules: source, technique, response action, precision, last tuned | `## Detections` in `memory.md`; `~/Clawic/data/cybersecurity/detections.md` past the threshold | One row per rule |
| Third parties assessed: tier, data they hold, access they have, review date | `## Vendors` in `memory.md`; `~/Clawic/data/cybersecurity/vendors.md` past the threshold | One row per vendor |
| Incidents: awareness timestamp, scope, actions, outcome, where the evidence lives | `~/Clawic/data/cybersecurity/incidents/<year>.md` | Append-only, cut by year, from the first incident |
| Standing indicators the user blocks or hunts for, with why and when they expire | `~/Clawic/data/cybersecurity/indicators.md` | One row per indicator; born as its own file because it is machine-shaped |
| Things you produced that get re-read — threat models, playbooks, post-incident reviews, policies, reports, diagrams | `~/Clawic/data/cybersecurity/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Recurring cadences: access review, key rotation, restore drill, tabletop, pentest, vendor reassessment, risk-acceptance expiry | `## Due` in `memory.md` | Fixed rows, dates updated |
| Hosts, servers, appliances | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| People you would call or notify: counsel, insurer, IR retainer, provider abuse desk, regulator, vendor security contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person |
| Domains, mail-authentication posture, certificate and registration expiry | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| Laptops, phones and other endpoints discovered or hardened | `~/Clawic/data/devices/devices.md` (**shared**) | One row per device |
| Cyber insurance policy and security tooling subscriptions | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per policy or subscription |
| A remediation programme the user tracks as work with a deadline | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| **Anything durable this table does not name** | `~/Clawic/data/cybersecurity/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials, tokens, keys, cookies, password hashes; raw evidence; personal records | Nowhere under `~/Clawic/data/` | Pointer, hash or count only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| Somebody first became aware of a possible incident | The incident row in `incidents/<year>.md`, starting with the awareness timestamp |
| An incident closed, or a post-incident review happened | The outcome in the incident row; the review itself in `artifacts/` |
| A finding was raised, or an owner accepted the risk | `## Findings`, with owner, due date and — for an acceptance — the expiry, plus a `## Due` row for that expiry |
| A system, trust boundary, crown-jewel asset or log source was identified | `## Environment` |
| A detection rule was written, tuned or retired | `## Detections` |
| A vendor was assessed or reassessed | `## Vendors`, and its next review date in `## Due` |
| An indicator has to be blocked or hunted beyond its own incident | `indicators.md` |
| A threat model, playbook, policy, report or diagram was produced | `artifacts/` |
| A host, appliance or server was discovered, hardened or retired | Its row in `servers.md` |
| Somebody was identified as a call-at-3am contact | Their row in `contacts.md` |
| A domain, its mail authentication, or a certificate expiry came up | Its row in `domains.md` |
| A laptop, phone or unmanaged device was discovered or brought into scope | Its row in `devices.md` |
| The cyber insurance policy or a security subscription was named | Its row in `subscriptions.md` |
| A recurring control was scheduled or run | `## Due` |
| The user declared a preference, or set the authorized scope | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, incidents, indicators and the shared inventories begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/cybersecurity/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts and incidents are the exception: a threat model, a playbook, a post-incident review or an incident timeline is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:OKTA_API_TOKEN` · `keychain:soc-svc` · `1password:Security/EDR-console` · `bitwarden:Security/SIEM` · `vault:kv/security/siem` · `ssm:/prod/db/password` · `secretsmanager:prod/api/key` · `profile:ir-readonly` · `file:~/.ssh/id_ed25519`

When the user pastes something to save — a runbook, a policy, an export, a `.env`, a command log, a captured request — replace each secret value before writing and leave the pointer visible: `password: <ssm:/prod/db/password>`. Say in one line that you did it.

Two rules specific to this domain, because security work is the one domain whose *evidence* is dense with both:

- **Evidence stays in the case store, never here.** Memory images, packet captures, mailbox exports, log dumps, malware samples and disk images live wherever the user's investigation keeps them; the memory file records the artifact's name, its hash, its custody chain and the path — a pointer, not the content. A sample copied into `~/Clawic/data/` is a live malicious file sitting in a folder nobody scans.
- **Personal data is summarized, never copied.** "412 customer records, name plus email plus order history, in the exported table" is the finding. The records are not.

In this domain — **not secrets, keep them**: hostnames, IP addresses, MAC addresses, staff usernames and email addresses, cloud account ids, ARNs and resource names, domain names, CVE and CWE ids, file hashes and other indicators, ATT&CK technique ids, ticket and case ids, rule names, port numbers, severity scores, certificate fingerprints, policy and case numbers. **Secrets, strip them**: passwords found during a review, password hashes (they are crackable authenticators), API keys and tokens, session cookies and bearer tokens, refresh tokens, private keys and passphrases, TOTP seeds and MFA recovery codes, connection strings carrying a password, webhook or pager URLs with an embedded token, and any credential recovered from an attacker's tooling.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [incidents/](#incidents) · [artifacts/](#artifacts) · [indicators.md](#indicatorsmd) · [shared inventories](#shared-inventories) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/cybersecurity/` if it does not exist.

```yaml
org_profile: smb
report_audience: mixed
containment_bias: evidence-first
severity_scale: kev-epss
remediation_sla_days: {critical: 7, high: 30, medium: 90, low: next-cycle}
siem_platform: sentinel
edr_platform: defender
primary_cloud: azure
compliance_regime: [soc2, gdpr]
authorized_scope_file: scope.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  ticketing: jira
  scanner: tenable
conventions:
  finding_id: "SEC-<year>-<n>"
platform:
  idp: entra
  ot_in_scope: false          # passive discovery only on that segment
safety_posture:
  live_commands: describe-only
exclusions:
  never_touch: [clinic-vlan, legacy-erp]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Cybersecurity Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Incidents (2026, 4) → `incidents/2026.md`; read at the start of any incident, and before calling anything a first occurrence
- Threat model, payments service → `artifacts/threat-model-payments.md`; read before any change to the payment path
- Ransomware playbook → `artifacts/playbook-ransomware.md`; read the moment encryption or extortion is suspected
- Standing indicators (23) → `indicators.md`; read when checking whether something is already known-bad
- Findings (21 open) → `findings.md`; read before raising a finding, so the same issue does not get a second id

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Privileged access review | quarter | 2026-04-14 | 2026-07-14 |
| Backup restore drill, timed | quarter | 2026-05-02 | 2026-08-02 |
| Tabletop exercise | year | 2025-11-18 | 2026-11-18 |
| KEV sweep against the estate | week | 2026-07-20 | 2026-07-27 |
| Risk acceptance SEC-2026-014 expires | once | — | 2026-09-30 |
| Vendor reassessment: mail gateway | year | 2026-02-09 | 2027-02-09 |

## Scope & Authorization
Owner: the user, sole director. In scope: their own cloud account, the office LAN, company laptops.
Out of scope: the clinic VLAN (medical devices, passive discovery only) and anything belonging to clients.
Disruption allowed: none during business hours; containment pre-approved on the user's own laptop.
Confirmed 2026-07-26. Long version: `~/Clawic/data/cybersecurity/scope.md`.

## Environment
### Crown Jewels
Customer database (PII, 40k rows) · the payment processor account · the code-signing key · the email tenant.
### Systems
Identity provider, 24 staff · one production cloud subscription · GitHub org, 31 repos · SIEM at 90-day retention.
### Trust Boundaries
Internet → CDN → gateway → app subnet → database subnet (no internet route).
Staff laptops → IdP → SaaS. Contractors reach GitHub only, through their own tenant.
### Log Sources
| Source | Retention | Covers | Gap |
|---|---|---|---|
| IdP sign-in and audit | 90 days | Identity | Mailbox item access needs the premium audit tier |
| EDR | 30 days raw | Endpoint execution | Nothing on the two Linux build servers |

## Findings
### Open
| Id | Finding | Severity | Attack path removed | Owner | Due | Status |
|----|---------|----------|---------------------|-------|-----|--------|
| SEC-2026-019 | Build server reachable from the office VLAN on 22 | high | Lateral movement to the signing key | user | 2026-08-12 | open |
### Risk Accepted
| Id | Risk | Accepted by | On | Expires | Compensating control |
|----|------|-------------|----|---------|----------------------|
| SEC-2026-014 | Legacy ERP cannot do MFA | user | 2026-06-30 | 2026-09-30 | Reachable from one jump host only, logged |

## Detections
| Rule | Source | Technique | Response | Precision (30d) | Last tuned |
|------|--------|-----------|----------|-----------------|------------|
| New inbox rule forwarding externally | Mail + audit logs | T1114.003 | Call the user, revoke sessions | 8/9 | 2026-06-11 |

## Vendors
| Vendor | Tier | Data they hold | Access they have | Last review | Next |
|--------|------|----------------|------------------|-------------|------|
| Mail gateway SaaS | critical | All inbound mail | OAuth app, mail.read | 2026-02-09 | 2027-02-09 |

## Pain Points
March 2026: a contractor's token stayed valid six weeks after offboarding. Sensitive to the leaver process since.

## How They Work
No security team. Wants the two things that matter this month, not a framework. Reads findings in the ticket, not in chat.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring control and every risk-acceptance expiry belongs here; an acceptance that lapses unnoticed is an unowned risk wearing a signature.
- **`## Scope & Authorization`** carries its confirmation date. Scope older than the last environment change is not scope: re-confirm rather than assume, and never widen it on inference.
- **`## Findings`**: ids are never reused, and a closed finding leaves `### Open` with its resolution recorded in the incident or artifact it belongs to — a register that only grows stops being triaged. `Attack path removed` is a required column: a finding that cannot fill it is a preference.
- **`## Environment`**: `Gap` is the most valuable column in the log-source table, because it is the list of questions you will not be able to answer during an incident.
- These headings are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still mapping their environment and their exposure |
| `complete` | Environment, crown jewels and log sources are known; the work is execution |

## incidents/

One file per year at `~/Clawic/data/cybersecurity/incidents/<year>.md`, from the first incident — a log grows without end and must never live inside `memory.md`.

```markdown
# Incidents — 2026

| Id | Aware at | Type | Affected | Scope confirmed | Containment | Outcome | Evidence |
|----|----------|------|----------|-----------------|-------------|---------|----------|
| INC-2026-03 | 2026-07-14 09:12 CEST | BEC | 1 mailbox | 1 mailbox, no admin role | Sessions revoked, rule deleted, hardware key enrolled | No funds moved; no notification clock triggered | Case store `ir/2026-03/`, audit export sha256:4b21… |

## INC-2026-03 — timeline
| When (UTC) | Source | Observed | Confidence |
|------------|--------|----------|------------|
| 2026-07-13 21:40 | IdP sign-in log | Successful sign-in, unmatched device id, hosting-provider ASN | confirmed |
| 2026-07-13 21:44 | Mailbox audit | Inbox rule created, moves replies containing "invoice" to RSS Feeds | confirmed |
| 2026-07-14 09:12 | User report | Colleague noticed a reply they never received | confirmed — awareness starts here |
```

- **`Aware at` is the legal clock** (SKILL.md, Notification Clocks). Write it with its timezone, in the first turn, before any analysis.
- Every timeline row carries its source and a confidence word from Rule 3. A row with no source is a hypothesis and belongs in prose, not in the table.
- The `Evidence` column is a location and a hash, never the evidence.
- People involved — counsel, the insurer's claims line, a vendor's security contact — go to `contacts.md` and are referenced here by name only.

## artifacts/

One file per thing, at `~/Clawic/data/cybersecurity/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **threat model**, **playbook** for a scenario, **post-incident review**, **policy or standard**, **report or board summary**, **network and data-flow diagram**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Threat model — payments service
*Read before any change to the payment path or its dependencies. Written 2026-07-26.*

Assets: card tokens, payout bank details, the webhook signing secret <1password:Eng/Payments/webhook>.
Entry points: public API, the processor's webhook, the admin panel, the CI deploy path.
Trust boundaries: internet→edge, app→database, CI→prod.
Top paths: (1) admin session theft → payout details changed; (2) forged webhook → false credit.
Controls present / missing / rejected, with the reason for each rejection.
```

```markdown
# Post-incident review — INC-2026-03
*Read before the next BEC, and before the next tabletop. 2026-07-20.*

What happened, in five lines. Timeline: `incidents/2026.md`.
Detection gap that let it run 12 hours: no alert on inbox-rule creation → now a rule (`detections.md`).
Two actions with owners and dates → also in `## Findings`.
What we would not do again: reset the password before revoking sessions.
```

If the user runs the remediation as a project, the summary and the owner also belong in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by name.

## indicators.md

Standing indicators only — the ones that outlive their incident because they get blocked or hunted repeatedly. Everything else stays in its incident timeline.

```markdown
# Indicators

| Indicator | Type | Source | Why kept | Added | Expires |
|-----------|------|--------|----------|-------|---------|
| 4b21…c9 | sha256 | INC-2026-03 attachment | Blocked at the mail gateway | 2026-07-14 | 2027-07-14 |
| invoice-portal-login[.]com | domain | INC-2026-03 phishing page | Blocked at DNS; lookalike of the real tenant | 2026-07-14 | 2027-07-14 |
```

Defang hostile domains and URLs (`[.]`) so nothing in the file is clickable by accident. Every indicator carries an expiry: addresses and domains get reassigned, and a list that never expires eventually generates false positives against innocent third parties. The expiry sweep is a `## Due` row.

## Shared inventories

These live outside the skill's folder and are shared with every other Clawic skill. The user may have none of those installed, so the format and the protocol travel with this skill. Three rules apply to all of them: **read the file before adding**, match on the identity key and **update that row in place** rather than appending a second one; **touch only rows this skill wrote** — a row from another source is adapted to, never rewritten; and if the file already exists with a different column set, **match its columns** and add anything missing as a trailing note, never rewriting its header. Amounts always carry their currency inside the value (`2400 EUR`), and estimates carry the date they were estimated.

### servers.md — `~/Clawic/data/servers/servers.md`

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| build-01 | hetzner | personal | fsn1 | CX32 | CI build and signing | 12 EUR | file:~/.ssh/id_ed25519 |
```

- Identity is `Name` + `Provider`. Update in place; never a second row for the same pair.
- Retirement is part of the inventory: when a host is decommissioned, delete its row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- Access reference is a pointer only — never a key, token or password.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If the folder already looks like that, follow it.
- Security state — baseline applied, EDR present, exposure — does not go in this header. It belongs in `## Environment`, keyed by the same host name.

### contacts.md — `~/Clawic/data/contacts/contacts.md`

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Marta Rey | marta@example-law.com | External counsel, data protection | email | Owns the breach-notification decision | 2026-07-14 | — |
| CyberCo claims | claims@cyberco.example | Insurer, 24/7 claims line | phone | Must be notified before any IR firm is engaged | 2026-02-01 | — |
```

- **Identity key**: lowercase email; failing that a handle; failing both, `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit. `Preferred channel` is the type of channel, not the address, and never serves as the key.
- The people this skill adds are the ones an incident needs: external counsel, the insurer's claims line, the IR retainer, an upstream provider's abuse desk, a regulator contact, a vendor's security contact, the internal decision-maker. `Context` says what decision they own — at 3am that is the only column that matters.
- Past 15 people, or as soon as one does not fit its row, one file per person at `~/Clawic/data/contacts/<name>.md`, with `contacts.md` kept as the index through the `File` column.
- Leaving = deleting the row and noting the date in `memory.md`. Stale emergency contacts are worse than none: they consume the first twenty minutes of an incident.

### domains.md — `~/Clawic/data/domains/domains.md`

```markdown
# Domains

| Domain | Registrar | Expires | Records of note | Notes |
|--------|-----------|---------|-----------------|-------|
| example.com | porkbun | 2027-03-04 | MX, SPF, DKIM s1, DMARC p=reject with rua | Registrar lock on; TLS cert expires 2026-10-02 |
```

- Identity is the domain name. This skill writes the mail-authentication posture (SPF, DKIM selectors, DMARC policy), registrar lock state and certificate expiry — each of which is either a control or an outage waiting for a date.
- Lookalike domains the user registered defensively go here with `Notes: defensive registration`. Lookalikes owned by somebody else are indicators, not domains: they go to `indicators.md`.
- **Scale cut**: past ~40 hostnames, group by apex into `<apex>.md` and keep `domains.md` as the index.
- Expiry dates that matter (domain, certificate) also get a `## Due` row — the inventory does not remind anybody by itself.

### devices.md — `~/Clawic/data/devices/devices.md`

```markdown
# Devices

| Device | Type | Owner | OS / version | Network | Notes |
|--------|------|-------|--------------|---------|-------|
| mbp-14-marta | laptop | Marta | macOS 15.5 | office-wifi | Disk encryption on, MDM enrolled, EDR present |
```

- Identity is the device name, falling back to the MAC address when there is no name. Update in place.
- This skill writes what decides an incident: disk encryption, MDM enrolment, EDR presence, OS version, and whether the device is managed at all. An unmanaged device found on the network is a finding *and* a row here.
- **Scale cut**: past 15 devices, one file per device and `devices.md` as the index. Above roughly that size the real inventory is an MDM export, and this file becomes the exceptions list.

### subscriptions.md — `~/Clawic/data/finances/subscriptions.md`

```markdown
# Subscriptions

| Name | Cost | Cycle | Renews | Account reference | Notes |
|------|------|-------|--------|-------------------|-------|
| CyberCo cyber liability | 2400 EUR | year | 2027-02-01 | policy CY-88213 | 1M EUR limit; 72h notice clause; panel counsel mandatory |
```

- Identity is the subscription name. This skill writes two kinds of row: the cyber insurance policy — whose notice clause and panel requirement change what may be done in the first hour — and security tooling the user pays for.
- Policy and account numbers are identifiers, not secrets, and belong here. The portal login does not: `1password:Insurance/CyberCo`.
- This file is a single table and does not split; a cancelled subscription has its row deleted and the date noted in `memory.md`.

### projects/ — `~/Clawic/data/projects/<project>.md`

One file per project, from the first. A remediation programme, a certification push or a hardening migration goes here when the user tracks it as work with a deadline; the security detail stays in this skill's boxes and is referenced by name. Closing is `status: done | cancelled — <date>` inside the file, never deletion — it is the record of what was delivered.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`assets.md` — `## Crown Jewels`, `## Systems`, `## Trust Boundaries`, `## Log Sources`. The log-source table with its `Gap` column is the reason this file exists: it is the pre-written answer to "can we even tell?".

`findings.md` — `## Open`, `## Risk Accepted`. Same columns, same id sequence. Nothing is deleted from `## Risk Accepted` at expiry: the row moves back to `## Open` with a new due date, because an expired acceptance is an open risk again.

`detections.md` — one row per rule with source, technique, response, precision and last-tuned date, plus a `## Retired` section holding what was removed and why. Retired rules matter: without that section, the same noisy rule gets re-enabled every year.

`vendors.md` — one row per third party with tier, data held, access granted, last review and next review. A vendor that holds data or holds a token is a trust boundary, and this is the list of them.
