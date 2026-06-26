# Business Impact Analysis (BIA) Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Business Continuity

## Purpose

Walks a business-continuity coordinator (BCMS owner) and process owners through a **Business Impact Analysis (BIA)** aligned to **ISO 22301:2019 clause 8.2.2** and **NIST SP 800-34 Rev. 1 Appendix A**. The BIA is the foundation of every downstream BCMS artefact — recovery strategies, business-continuity plans, IT disaster-recovery scope, vendor-criticality tiering, crisis-management runbooks, and tabletop / live-exercise scope. The skill captures the business-process inventory and ownership; runs multi-dimensional impact-over-time scoring (financial, regulatory, contractual / SLA, customer / reputational, life-safety, operational, workforce); derives **RTO / RPO / MTPD / MBCO / WRT** with the ISO 22301 discipline **RTO < MTPD**; maps upstream-and-downstream dependencies (applications, data, vendors, people / skills, facilities, equipment, utilities, network, identity); flags single points of failure; runs a current-capability-vs-requirement gap analysis; and produces a DRAFT BIA register, criticality-tier list, recovery-objective set, dependency map, gap list, recovery-strategy candidate list, validation-interview log, and steering-committee review-and-sign-off block.

## When to Use

- Initial BIA for a new business unit, subsidiary, acquired entity, or new product line entering the BCMS
- Annual BIA refresh required by ISO 22301:2019 clause 8.2.2, FFIEC BCM, OSFI E-21, APRA CPS 230, or DORA (where applicable)
- Triggered BIA after a major business change — re-organisation, ERP migration, cloud migration, vendor change, M&A integration, regulatory-perimeter change
- Pre-tabletop / pre-live-exercise scope-setting BIA
- Recovery-strategy review where the steering committee asks "have our RTOs kept pace with the business?"
- Vendor-criticality re-tier exercise where a Tier-1 BPO / SaaS provider has changed
- Audit response (internal audit, external assurance, regulator BCM examination)

## What It Does

**Phase 1: Scoping and BCMS Frame**
1. Captures organisation, in-scope entity / business unit / location, BCMS owner, BIA sponsor, regulatory frame (ISO 22301 / NIST 800-34 / FFIEC BCM / DORA / Solvency II / HIPAA Security Rule / OSFI E-21 / APRA CPS 230), BIA cycle (initial / annual / triggered), corporate impact rubric and risk-tolerance bands, and steering-committee roster

**Phase 2: Process Inventory**
2. Captures business processes — name, single accountable owner, customer of the process, products / services supported, outputs, peak-period and off-peak posture, regulatory / contractual obligations attached, and ownership-evidence trail

**Phase 3: Impact-Over-Time Scoring**
3. Scores each process across seven dimensions — financial, regulatory, contractual / SLA, customer / reputational, life-safety, operational, workforce — at the corporate impact-time horizons (0–4h, 4–24h, 1–3d, 3–7d, 1–2w, 2–4w, 4w+) with the highest dimension setting the row severity

**Phase 4: Recovery Objectives**
4. Derives **RTO** where impact crosses the MTPD-equivalent threshold, records **MTPD**, defines **MBCO** (Minimum Business Continuity Objective), derives **RPO** from data-loss tolerance, derives **WRT** for application-recovery hand-off, and enforces the ISO 22301 discipline **RTO < MTPD**

**Phase 5: Dependency Mapping**
5. Maps upstream-and-downstream applications, data stores, third-party vendors and BPO providers with criticality tier, people / skills, facilities, equipment, utilities, network, identity, key-management; flags cross-process shared dependencies that constitute single points of failure (SPOF)

**Phase 6: Gap Analysis**
6. Compares current recovery capability (backup posture, replication topology, alternate site, vendor SLA, workforce cross-training, paper / manual workaround feasibility, escalation contact tree) against the derived RTO / RPO / MBCO; lists named gaps with single owner and target close date

**Phase 7: BIA Assembly**
7. Produces a criticality-tier list (Tier 1 / 2 / 3 / 4 / out-of-scope), DRAFT BIA register, recovery-objective set, dependency map, gap list, recovery-strategy candidate list, validation-interview log, and steering-committee review-and-sign-off block

## Output

A DRAFT BIA package with:
- BIA register (one row per process, with owner, dimensions, impact-over-time scores, RTO / RPO / MTPD / MBCO / WRT, criticality tier)
- Criticality-tier list (Tier 1 / 2 / 3 / 4 / out-of-scope, sorted by tier then RTO ascending)
- Recovery-objective set (RTO, RPO, MTPD, MBCO, WRT for every Tier-1 and Tier-2 process)
- Dependency map (applications, data, vendors, people / skills, facilities, equipment, utilities, network, identity, key-management) with SPOF flags
- Gap list (current capability vs. requirement, single owner, target close date, target evidence)
- Recovery-strategy candidate list (in-house redundancy, alternate site, vendor diversification, manual workaround, defer-and-reconstitute) flagged for the steering committee
- Validation-interview log (process owner, interview date, evidence reviewed, open questions)
- Steering-committee review-and-sign-off block
- Open-questions / unresolved-information list

## Notes

This skill **drafts** the BIA to support — never replace — the steering committee's adoption of recovery objectives and the BCMS owner's downstream artefacts (recovery strategy, BCPs, DR plan, exercise scope). The skill does **not** authorise a recovery investment, does **not** approve a recovery strategy, does **not** set a vendor's contractual SLA, does **not** declare an incident or invoke a BCP, does **not** replace the IT disaster-recovery test programme, and does **not** opine on the regulator's adequacy view of the BCMS. The skill enforces the **ISO 22301 RTO < MTPD discipline** and refuses to record an RTO that equals or exceeds MTPD without an explicit steering-committee acceptance note.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
