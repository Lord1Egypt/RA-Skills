# DQF Driver Qualification File Audit

**Platforms:** Claude · Openclaw · Codex
**Domain:** Motor-Carrier Safety — Driver Qualification Files under 49 CFR § 391

## Purpose

A DQF pre-audit partner for DOT-regulated motor-carrier safety directors, DOT compliance managers, third-party DQF administrators, and HR safety staff. Turns the contents of each driver's qualification file into a DRAFT per-driver findings report aligned with 49 CFR § 391 — flagging missing, expired, or non-conforming documents with the controlling subsection cite, generating prioritized remediation actions (CRITICAL / HIGH / MEDIUM), and rolling per-driver findings into a fleet-level audit-readiness summary for the DOT-designated employer representative.

## When to Use

- Pre-audit review before an FMCSA Safety Audit, Compliance Review, or Investigative Safety Audit
- Onboarding a new driver and confirming the DQF is complete on day one
- Annual fleet-wide DQF review (driving record review under § 391.25 + § 391.27 certificate of violations)
- Mock-audit / "scan for fines" sweep — DQF violations average ~17% of all FMCSA violations and start at $1,000 / driver
- Implementing the **January 10, 2026** transition from paper Medical Examiner's Certificates to **CDLIS** electronic verification for CDL drivers
- Confirming Drug & Alcohol Clearinghouse compliance (pre-employment full query + annual limited query with driver consent)
- Onboarding an entry-level driver and confirming the **ELDT certificate** (CDL Class A/B upgrade, initial issuance, school-bus / passenger / hazmat endorsement) is on file before the CLP→CDL skills test

## What It Does

**Phase 1: Fleet and driver intake**
1. Captures carrier USDOT #, operating authority class (Property / Passenger / HM), interstate vs. intrastate posture, the DOT-designated employer representative (DER), and the audit purpose (pre-audit / onboarding / annual review / new-driver onboarding)
2. Captures the driver roster — for each driver: name (or internal ID), CDL class + endorsements / restrictions, hire date, status (active / leave / terminated), license-issuing state(s) within last 3 years

**Phase 2: Per-driver document review**
For each driver, walks through the § 391 documents in order:

| # | Document | Cite | Common failure |
|---|---|---|---|
| 1 | Employment application — 3-year employment / 10-year CMV employment history, accident history, gaps explained | § 391.21 | Gaps not explained; addresses missing |
| 2 | Inquiry into driving record — every state held a license in past 3 years (pre-employment MVR) | § 391.23 | Single-state pull; missing one state |
| 3 | Safety performance history — prior DOT employers in past 3 years; documented attempts where no response | § 391.23 | No documented attempts; older than 30 days into employment |
| 4 | Road test certificate or **CDL substitute** (per § 391.33) | § 391.31 / § 391.33 | Missing substitute; expired road-test certificate |
| 5 | Medical Examiner's Certificate — **CDLIS verification** for CDL drivers (post Jan 10, 2026); paper for non-CDL or grandfathered | § 391.41 / § 391.43 / § 391.45 / § 391.51 | Paper card for CDL driver post-2026; expired (max 24 months, often less); SPE / Skill Performance Evaluation not in file |
| 6 | Medical examiner — listed on FMCSA **National Registry of Certified Medical Examiners** | § 391.43 | Examiner not on Registry |
| 7 | Annual MVR + § 391.25 review (review note, reviewer signature, date) | § 391.25 | MVR pulled but no review note |
| 8 | Annual Certificate of Violations | § 391.27 | Missing; not signed by driver |
| 9 | Drug & Alcohol Clearinghouse — pre-employment **full** query with driver written consent | § 382.701(a) | Limited query only; consent missing |
| 10 | Drug & Alcohol Clearinghouse — annual **limited** query with general consent | § 382.701(b) | Missed annual due date |
| 11 | DOT pre-employment drug test result (negative) before performing safety-sensitive function | § 382.301 | Result not in file; driver dispatched before result |
| 12 | DOT random testing pool enrollment + selection records | § 382.305 / § 40.25 | Driver not in pool |
| 13 | Entry-Level Driver Training (**ELDT**) certificate from FMCSA Training Provider Registry — Class A / B initial, Class B-to-A upgrade, P / S / H endorsement initial | § 380.609 / § 380 Subpart F | Self-issued certificate; provider not on TPR |
| 14 | HazMat endorsement — TSA Threat Assessment, fingerprint, knowledge test | 49 CFR § 1572 | Missing TSA letter |
| 15 | Longer Combination Vehicle (LCV) training & certification | § 380 Subpart B | Driver pulls LCV without certificate |
| 16 | Disqualifying conviction tracking under § 383.51 / § 391.15 | § 383.51 / § 391.15 | Disqualifying conviction not actioned |
| 17 | Driver's signed receipt of carrier's policies (D&A, fatigue, distracted driving, post-accident testing) | § 382.601 / company policy | Receipt missing |
| 18 | Termination / retention markers (employment + 3 years retention; safety performance history retention) | § 391.51 / § 379 | File destroyed before retention period |

**Phase 3: Findings, remediation, and rollup**
3. For each finding, assign a priority:
   - **CRITICAL — ≤ 7 days** (driver should not be dispatched until cured; e.g., expired MEC, no negative pre-employment drug test, no Clearinghouse pre-employment query, disqualifying conviction, ELDT missing for entry-level CDL skills test)
   - **HIGH — ≤ 30 days** (e.g., missing annual MVR review note, missing annual Certificate of Violations, missing annual Clearinghouse limited query, paper MEC for CDL driver post-2026)
   - **MEDIUM — ≤ 90 days** (e.g., gaps in employment history explanation, unsigned policy receipt)
4. Rolls per-driver findings into a fleet-level summary (drivers with CRITICAL count, % drivers with complete DQF, total estimated exposure per § 521 penalty schedule **as informational only — not a legal opinion**)
5. Produces a sign-off block for the DOT-designated employer representative

## Output

A DRAFT DQF audit packet with:

- Carrier identification block (USDOT #, authority class, DER name)
- Per-driver findings report — one per driver — with:
  - Document checklist (present / missing / expired / non-conforming, with cite)
  - Findings list with priority + recommended remediation
  - Retention status (employment + 3 years)
- Fleet-level rollup (drivers reviewed, CRITICAL count by category, top 5 systemic issues, estimated exposure note)
- "Immediate action" list (drivers who should not be dispatched until cured)
- Cited-regulation appendix (every cite used)
- DER sign-off block (designated employer representative certification)

## Safety

This skill produces a DRAFT pre-audit review, **not** an FMCSA submission, an official record of compliance, or a legal opinion. Every output is labeled **DRAFT — DOT-DESIGNATED EMPLOYER REPRESENTATIVE MUST REVIEW AND CERTIFY BEFORE TREATING AS A COMPLIANCE RECORD; NOT A SUBSTITUTE FOR LEGAL OR FMCSA-AUTHORIZED COMPLIANCE OFFICER REVIEW**. The skill never files or alters the official DQF, never logs into the Drug & Alcohol Clearinghouse, never queries CDLIS, never queries the FMCSA Portal, and never communicates with FMCSA, a previous employer, or a state DMV on the user's behalf. The skill enforces strict PII discipline: it works with driver internal IDs and last-4 of CDL where possible; full CDL numbers, SSNs, and medical-history details belong in the source DQF (under § 391.51 retention and confidentiality), not in working notes or chat output. The skill does **not** substitute for the carrier's controlled-substances and alcohol testing program administrator, the carrier's Designated Employer Representative, the carrier's safety attorney, or an FMCSA-authorized compliance officer. The estimated exposure number is informational only and is **not** a legal opinion or a representation that penalties will or will not issue. The skill does not provide medical opinions on driver fitness; medical determinations remain with the Certified Medical Examiner on the FMCSA National Registry.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
