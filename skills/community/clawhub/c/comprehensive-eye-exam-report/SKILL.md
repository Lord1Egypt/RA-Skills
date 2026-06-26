---
name: comprehensive-eye-exam-report
description: >
  Use this skill when a Doctor of Optometry (OD), optometric resident, or clinical
  documentation specialist needs to draft a comprehensive eye exam report from encounter
  data. Covers visual acuity, refraction, binocular vision, anterior and posterior segment
  findings, IOP, AOA-aligned diagnoses, and treatment or referral plan. Produces a DRAFT
  report for licensed OD review before any prescription issuance or medical record entry.
---

# Comprehensive Eye Exam Report

Converts raw encounter data into a structured, AOA-aligned comprehensive eye exam report for licensed OD review. Covers every section from entering visual acuity through the treatment plan and produces a DRAFT ready for signature and medical record entry.

---

## Before You Start

This skill produces **DRAFT documentation only**. All content requires review and signature by a licensed Doctor of Optometry before:
- Any spectacle or contact lens prescription is issued
- Any content enters the medical record or is transmitted to a payer
- Any referral is initiated

**PII rule:** Collect initials and year of birth only. Never record full name, date of birth, MRN, or insurance information in this conversation.

---

## Flow

### Phase 1 — Encounter Identification

Ask one question at a time. Collect:
1. Patient initials and year of birth (initials + YOB only)
2. Exam date and encounter type: New patient comprehensive (CPT 92004) or Established patient comprehensive (CPT 92014)
3. Chief complaint or reason for visit
4. Pertinent ocular and medical history (conditions, medications, allergies, family history)
5. Last eye exam date (if known)

Confirm all fields before proceeding. Flag any missing history as **[HISTORY GAP — CONFIRM WITH PATIENT]**.

---

### Phase 2 — Entering Visual Acuity

Collect entering (uncorrected or with current correction) visual acuity for each eye:

| Field | OD (Right) | OS (Left) | OU (Both) |
|-------|-----------|-----------|-----------|
| Distance VA (entering) | | | |
| Pinhole VA (if reduced) | | | |
| Near VA (if tested) | | | |
| Correction worn (Sc / CC / Plano) | | | |

Flag any entering VA worse than 20/40 in either eye as **[REDUCED VA — CLINICAL REVIEW REQUIRED]**.

---

### Phase 3 — Manifest Refraction

Collect manifest refraction results:

| Field | OD | OS |
|-------|-----|-----|
| Sphere | | |
| Cylinder | | |
| Axis | | |
| Add (if presbyopia) | | |
| BCVA (best corrected VA) | | |
| Prism (if prescribed) | | |

If BCVA does not reach 20/20 in either eye, flag **[REDUCED BCVA — DOCUMENT CAUSE; REFERRAL MAY BE INDICATED]**.

Collect subjective refinement notes if provided.

---

### Phase 4 — Binocular Vision and Ocular Motility

Collect:
- Cover test (distance and near): ortho / exophoria / esophoria / tropia — size in prism diopters if measured
- Near point of convergence (NPC): break and recovery
- Extraocular movements (EOM): full / restricted — specify direction if restricted
- Stereopsis (if tested): specify test and result

Flag any tropia, NPC > 10 cm, or EOM restriction as **[BINOCULAR VISION FINDING — DOCUMENT AND CONSIDER REFERRAL]**.

---

### Phase 5 — Anterior Segment (Slit-Lamp Biomicroscopy)

Collect findings for each structure. Use "WNL" (within normal limits) if normal. Specify abnormalities precisely.

| Structure | OD | OS |
|-----------|-----|-----|
| Lids and lashes | | |
| Conjunctiva and sclera | | |
| Cornea | | |
| Anterior chamber (depth, reaction) | | |
| Iris | | |
| Lens (nuclear, cortical, PSC grading if applicable) | | |

Flag any: corneal abrasion, active uveitis, anterior chamber cell or flare, acute-angle-closure signs (shallow AC, mid-dilated fixed pupil, corneal edema) as **[URGENT — IMMEDIATE CLINICAL ACTION REQUIRED]**.

---

### Phase 6 — Intraocular Pressure (IOP)

Collect:
- Instrument used (GAT / iCare / non-contact tonometer / Tono-Pen)
- OD: \_\_\_ mmHg at \_\_\_ (time)
- OS: \_\_\_ mmHg at \_\_\_ (time)
- Central corneal thickness (CCT) if measured

Flag:
- IOP ≥ 22 mmHg (either eye): **[ELEVATED IOP — GLAUCOMA EVALUATION INDICATED]**
- Asymmetry ≥ 4 mmHg: **[IOP ASYMMETRY — CLINICAL REVIEW REQUIRED]**
- IOP ≤ 5 mmHg: **[LOW IOP — RULE OUT HYPOTONY]**

---

### Phase 7 — Posterior Segment (Fundus Examination)

Collect method (BIO / 78D / 90D / fundus camera) and dilation status (dilated / undilated).

| Structure | OD | OS |
|-----------|-----|-----|
| Optic disc (color, margins, contour) | | |
| Cup/disc ratio (vertical) | | |
| Vessels (A/V ratio, crossing changes) | | |
| Macula (foveal reflex, drusen, pigment changes) | | |
| Peripheral retina (tears, detachment, lattice) | | |
| Vitreous | | |

Flag the following as **[MEDICAL REFERRAL FLAG]**:
- C/D ratio ≥ 0.6 or C/D asymmetry ≥ 0.2: suspect glaucoma
- Disc edema or pallor
- Subretinal fluid, macular edema, or suspected neovascularization
- Peripheral retinal tear or detachment: **[URGENT — SAME-DAY OPHTHALMOLOGY REFERRAL]**
- Diabetic retinopathy (any grade beyond mild NPDR)
- Macular degeneration (wet or advanced dry)

---

### Phase 8 — Ancillary Testing (If Obtained)

For each test obtained, collect:
- OCT (optic nerve, macula, or anterior segment): specify findings and comparison to prior if available
- Humphrey Visual Field (24-2 or 10-2): MD, PSD, GHT, reliability indices
- Fundus photography: confirm documentation
- Corneal topography: specify pattern and Ks if collected
- Other (specify)

Label all ancillary results: **[ANCILLARY TEST — PRELIMINARY INTERPRETATION; OD REVIEW REQUIRED]**

---

### Phase 9 — Assessment

Collect the assessment from the OD:

1. Primary diagnosis (ICD-10 code and description)
2. Secondary diagnoses (up to 5, each with ICD-10 code)
3. Medical referral flags triggered (from Phases 2–8 above)
4. Clinical impressions or notes

Confirm that any flagged urgent or medical referral condition has a documented plan in Phase 10.

---

### Phase 10 — Plan

Collect the treatment and follow-up plan:

- **Spectacle Rx:** Issue new / No change / Not indicated (reference Phase 3 refraction)
- **Contact lens Rx:** New fit / Refit / Continuation / Not indicated
- **Medical treatment:** (medications, procedures — OD enters)
- **Referrals:** Ophthalmology / Neurology / PCP / Other — specify urgency and reason
- **Patient education:** (topics discussed)
- **Follow-up:** \_\_\_ months / As needed / sooner if symptoms

Any **[MEDICAL REFERRAL FLAG]** from Phases 5–7 must have a corresponding referral in this section or a documented clinical reason for deferral.

---

### Phase 11 — DRAFT Report Assembly

Compile all phases into the following structured report:

```
COMPREHENSIVE EYE EXAMINATION — DRAFT
Patient: [Initials] | YOB: [Year] | Date: [Exam Date]
Encounter Type: [CPT code and description]
Chief Complaint: [From Phase 1]

OCULAR HISTORY: [From Phase 1]
MEDICAL HISTORY / MEDICATIONS / ALLERGIES: [From Phase 1]

VISUAL ACUITY (ENTERING): [Table from Phase 2]
MANIFEST REFRACTION: [Table from Phase 3]
  BCVA: OD [VA] OS [VA]

BINOCULAR VISION / OCULAR MOTILITY: [From Phase 4]

ANTERIOR SEGMENT (SL BIO): [Table from Phase 5]

INTRAOCULAR PRESSURE: [From Phase 6]
  Instrument: [Method and time]

POSTERIOR SEGMENT: [Table from Phase 7]
  Dilation: [Yes/No — agent if dilated]

ANCILLARY TESTING: [From Phase 8 — if obtained]

ASSESSMENT:
  1. [Primary diagnosis — ICD-10]
  2. [Secondary diagnoses — ICD-10]
  [Medical referral flags if triggered]

PLAN:
  Spectacle Rx: [Status]
  Contact Lens Rx: [Status]
  Treatment: [If applicable]
  Referrals: [If applicable]
  Patient Education: [Topics]
  Return: [Interval]

─────────────────────────────────────────
DRAFT — FOR LICENSED OD REVIEW ONLY
This document is not finalized and must not be used for prescription issuance,
medical record entry, billing, or referral until reviewed and signed by a
licensed Doctor of Optometry.

Reviewing OD: _________________________ License No.: _____________
Signature: ____________________________ Date: ___________________
─────────────────────────────────────────
```

Present the complete DRAFT to the user. List any open items or flagged issues that require OD attention before finalization.

---

## Key Rules

- **Never issue a prescription.** The skill drafts documentation; the licensed OD issues prescriptions.
- **Never finalize the report.** Every output is labeled DRAFT until the OD reviews and signs.
- **Medical referral flags are mandatory.** Any finding meeting a flag criterion in Phases 2–7 must appear in the Assessment and be addressed in the Plan.
- **Applicable standards:** Use AOA clinical practice guidelines for diagnosis terminology and classification. Do not invent diagnoses.
- **ICD-10 codes:** Prompt for codes but label them **[OD TO CONFIRM ICD-10]** if not confirmed by the clinician.
- **PII:** Collect initials + year of birth only. Immediately flag and stop if the user provides a full name, date of birth, MRN, or insurance number; do not record it.
- **Urgent flags:** Any finding flagged URGENT must be surfaced to the OD immediately, not buried in the report.

---

## Output Format

The final output is a single structured DRAFT report (as defined in Phase 11) plus:
- A numbered open-items list of any flags or gaps requiring OD attention
- A note confirming the report is DRAFT and must not be used until OD review is complete

---

## Feedback

If the user expresses an unmet need, a workflow gap, or dissatisfaction with the skill, surface the contribution link:
[Open an issue on GitHub](https://github.com/archlab-space/Open-Skill-Hub/issues)
