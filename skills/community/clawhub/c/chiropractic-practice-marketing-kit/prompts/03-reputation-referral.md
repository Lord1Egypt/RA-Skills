# Prompt 3 — Reputation Management + B2B Referral

## System Context

All 7 compliance gates enforced. Additional context for reputation management:
- **FTC 2023 review rules:** No review gating (showing only positive reviews); no incentivized reviews (discount, gift card, free visit in exchange for a review = FTC violation); reviews may be requested but cannot be steered
- **HIPAA in responses:** GBP responses to patient reviews may not confirm that the reviewer is a patient, confirm a diagnosis, confirm a treatment, or include any PHI — even to defend a negative review. Acknowledge concern and offer to discuss privately.

---

## Prompt 3A — Review Request Sequence

```
Generate a 3-touchpoint FTC 2023-compliant review request sequence for a Nevada chiropractic practice.

Practice: [PRACTICE NAME], [CITY NV] — [DC NAME] DC
Review platforms: [Google / Healthgrades / Yelp — list platforms]

Touchpoint 1 — In-office verbal script (end of visit, for staff):
- Natural, non-pressured request
- NO: "leave us a 5-star review"
- NO: offer of incentive for review
- YES: "if you had a good experience, sharing it on Google helps other patients find us"

Touchpoint 2 — Post-visit SMS or email (24–48 hours after visit):
- FTC 2023 compliant
- No steering to star rating
- No incentive language
- TCPA opt-out if SMS
- 160 characters max if SMS

Touchpoint 3 — 2-week follow-up (if no review received):
- Single follow-up only (no review bombardment)
- Soft ask
- Provide direct review link
- HIPAA: do not reference specific treatment or condition in the message
```

---

## Prompt 3B — GBP Response Templates (15 Templates)

```
Generate 15 Google Business Profile response templates for a Nevada chiropractic practice.

Practice: [PRACTICE NAME] — [DC NAME] DC

HIPAA rule for all responses: Do NOT confirm the reviewer is a patient, confirm any diagnosis, reference any treatment, or include any health information — even when responding to a negative review about a specific condition.

Group 1 — Medicare/Insurance Billing Complaints (5 templates):
1. "Medicare didn't cover what they said" complaint — acknowledge; invite private conversation; do NOT confirm services billed or coverage decisions
2. "Insurance denied my claim" complaint — same HIPAA rule; explain coverage verification process generally
3. "I was billed for something I thought was covered" — acknowledge billing team contact info; no PHI
4. "They charge too much for what Medicare covers" — Medicare Part B coverage explanation (spinal manipulation only) without confirming specific services
5. "I thought the consultation was free" — new patient process explanation without PHI

Group 2 — Credential/Scope Complaints (2 templates):
6. "The chiropractor said they could treat my [condition] but couldn't" — acknowledge concern; scope explanation without confirming clinical discussion; HIPAA safe
7. "I expected more from a 'board certified' doctor" — credential explanation; offer private resolution

Group 3 — Personal Injury / Billing Disputes (2 templates):
8. "My PI lien was higher than I expected at settlement" — lien process explanation without PHI; invite billing coordinator contact
9. "They said my workers' comp was covered but it wasn't" — workers' comp authorization process explanation; no PHI confirmation

Group 4 — Positive Review Responses (4 templates):
10. Sports injury recovery positive review
11. New patient first-visit positive review
12. Long-term maintenance care patient positive review
13. Auto accident recovery positive review (HIPAA: do not confirm PI case or treatment)

Group 5 — General Concern (2 templates):
14. Wait time complaint
15. Front desk / communication complaint
```

---

## Prompt 3C — B2B Referral Letters (6 Letters)

```
Generate 6 B2B referral relationship letters for a Nevada chiropractic practice.

Practice: [PRACTICE NAME], [DC NAME] DC[, CREDENTIALS]
Address / Phone / Website: [INFO]

Letter 1 — Primary Care Physician (Musculoskeletal Co-Management):
- Audience: Clark County PCPs and internal medicine physicians
- Angle: Chiropractic as evidence-based first-line intervention for musculoskeletal back and neck pain (cite CPGs: ACP 2017 guidelines recommending non-pharmacologic treatment first)
- No referral fee language; no kickback implication
- Offer: complimentary consultation report for referred patients

Letter 2 — Orthopedic Surgeon (Pre/Post-Surgical Rehabilitation):
- Audience: Orthopedic surgeons, spine surgeons in Clark County
- Angle: Pre-surgical conditioning + post-surgical rehabilitation within chiropractic scope; CPT 97140/97530 co-management
- No "we treat what surgeons can't" language (scope safe)

Letter 3 — Personal Injury Attorney (Lien-Based Referral — PI practices only):
- CRITICAL: NO referral fee language; NO "we'll refer our patients to you" language; NO value exchange implication
- NRS 7 (Nevada attorney advertising/referral rules) compliance
- Angle: professional introduction; describe compliant PI lien process; offer documentation support for attorney clients
- Tone: informational, not transactional

Letter 4 — Workers' Compensation Case Manager / TPA:
- Audience: Clark County workers' comp case managers, TPAs, employer HR
- Angle: Evidence-based chiropractic for work injury; early intervention reduces long-term disability costs
- Authorization process explanation; no "always covered" claims

Letter 5 — OB/GYN (Prenatal Chiropractic — Webster technique only):
- Generate only if Webster Technique certification confirmed
- Audience: Henderson/Las Vegas OB/GYN practices
- Webster Technique: ICPA certification required in letter; correct framing (sacral analysis and adjustment; not "treats breech")
- Offer: consultation note to referring OB/GYN after each prenatal visit

Letter 6 — Corporate HR / Employee Wellness Program:
- Audience: Clark County HR departments, self-insured employer wellness programs
- Angle: Musculoskeletal health = reduced lost work days; preventive adjustment for desk workers
- Group rate offer structure (compliant with NVBCE advertising rules — no "guaranteed results" group discount)
```
