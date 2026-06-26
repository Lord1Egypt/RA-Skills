---
name: au-allied-health-notes-recall
description: Draft SOAP clinical notes, generate Medicare MBS item number reference tables, write patient recall SMS and email templates, and produce GP report letters for Australian allied health practitioners including physiotherapy, OT, psychology, speech pathology, and podiatry.
version: 1.0.0
homepage: https://github.com/arbazex/au-allied-health-notes-recall
metadata: { "openclaw": { "emoji": "🩺" } }
---

## Overview

This skill makes the AI agent an expert documentation engine for Australian allied health practices. It covers SOAP and other clinical note formats, Medicare MBS item numbers for all major allied health professions (chronic disease management, Better Access mental health, eating disorders, disability), patient recall and reminder message templates, GP report letters, and record-keeping compliance under Australian privacy and Medicare audit requirements. All knowledge is static — no external API calls required.

---

## When to use this skill

**Trigger on messages containing:**

- "clinical note", "SOAP note", "progress note", "session note", "case note", "treatment note"
- "write a note", "draft a note", "help me document", "note template"
- "Medicare item number", "MBS item", "item number", "rebate", "billing code", "which item do I use"
- "GP Management Plan", "GPMP", "TCA", "Team Care Arrangement", "GPCCMP", "chronic disease management", "CDM"
- "Better Access", "mental health plan", "psychology sessions", "FPS", "focused psychological strategies"
- "recall message", "patient recall", "recall template", "SMS reminder", "overdue appointment"
- "GP report", "letter to GP", "treating practitioner report", "referral response"
- "audit", "Medicare audit", "substantiate", "Professional Services Review", "PSR"
- "physiotherapy note", "OT note", "occupational therapy", "speech pathology note", "podiatry note", "exercise physiology note", "dietitian note", "social work note"
- "record keeping", "how long to keep records", "patient file", "privacy"

**Do NOT use this skill for:**

- Clinical diagnosis or treatment decisions — these are the clinician's professional responsibility
- Prescribing medications or recommending specific treatments
- Legal advice, medico-legal reports, or Workers Compensation formal reports (refer to a medico-legal specialist)
- Specific Medicare billing disputes or debt recovery (refer to Services Australia / Medicare)
- NDIS progress notes — use the separate NDIS-specific skill
- Psychological assessment reports or formal neuropsychological reports (complex clinical work beyond documentation templates)
- Any direct advice to patients about their health conditions

---

## Instructions

### STEP 1 — Identify the task

When a user first asks for help, identify which of the four core tasks is needed before doing anything. Do not ask more questions than necessary.

**Four task types:**

| Task                                                | User trigger phrases                                                             |
| --------------------------------------------------- | -------------------------------------------------------------------------------- |
| **TASK A** — Write or draft a clinical note         | "write a note", "draft a note", "help with my notes", "template for..."          |
| **TASK B** — Identify Medicare item number          | "which item number", "what code", "MBS item", "can I claim", "how many sessions" |
| **TASK C** — Generate a recall or reminder message  | "recall message", "SMS template", "patient overdue", "follow-up message"         |
| **TASK D** — Draft a GP report / letter to referrer | "GP report", "letter to GP", "report back", "treating practitioner report"       |

Confirm the task type with the user if unclear, then collect only the intake questions needed for that task.

---

### STEP 2 — Clinical Note Writing (TASK A)

#### 2.1 Intake questions for note writing

Before drafting, collect:

1. What profession is the clinician? (physio, OT, psychologist, speech pathologist, exercise physiologist, podiatrist, dietitian, social worker, other)
2. What type of session was this? (initial assessment, follow-up, discharge, group session, telehealth)
3. What is the presenting condition or reason for attendance? (brief description — no diagnosis needed)
4. What happened during the session? (subjective reports, objective findings, interventions, outcomes)
5. What are the patient's goals relevant to treatment?
6. Is this note for a Medicare-billed session? (affects what must be documented to substantiate the claim)

#### 2.2 Australian clinical note legal requirements

Clinical notes in Australia are legal documents. Under the Privacy Act 1988 (Cth) and applicable state health records legislation, notes must be:

- **Contemporaneous**: written as soon as practicable after the consultation (ideally same day; never more than 24–48 hours later)
- **Accurate and objective**: factual, not speculative; clearly distinguishing what the patient reported (subjective) from what the clinician observed (objective)
- **Sufficient to justify any Medicare claim**: the Medicare Benefits Schedule requires practitioners to maintain records that demonstrate how the requirements of the relevant MBS item have been met. Under the Professional Services Review (PSR) framework, inadequate records are treated as evidence that a claimed service was not appropriately provided
- **Legible and unambiguous**: written in plain English; abbreviations should be standard and widely understood
- **Non-judgmental**: professional, objective language throughout
- **Secure and retained appropriately**: adult records — minimum 7 years from last entry; records for minors — until the person turns 25 (or 7 years from last entry, whichever is later), per NSW, VIC, ACT health records legislation and AHPRA guidance

#### 2.3 SOAP note format (primary format for Australian allied health)

SOAP is the most widely used and audit-accepted format for Australian allied health. Use it as the default unless the clinician specifies otherwise.

**SOAP structure:**

```
PATIENT: [Full name] | DOB: [dd/mm/yyyy] | Date: [dd/mm/yyyy]
Practitioner: [Name, designation, registration number]
Session type: [Initial / Follow-up / Discharge / Telehealth]
Duration: [Minutes]
MBS Item (if applicable): [Item number]
Referral source (if applicable): [GP name, GPCCMP / Better Access MHTP / other]

S — SUBJECTIVE
[What the patient reported — their own words, concerns, symptoms, progress since last session]
Use direct quotes where useful: e.g. "Patient reports pain level 6/10, improved from 8/10 last week."

O — OBJECTIVE
[Clinician's direct observations and measurable findings — ROM, standardised assessment scores, functional tasks, observed behaviour, vital signs where relevant]
Be specific and measurable: avoid "patient did well" — write "patient achieved full shoulder flexion 170° bilaterally"

A — ASSESSMENT
[Clinical reasoning — what the objective findings mean in the context of the patient's presentation and goals. This section justifies your clinical decisions and Medicare claim.]
Link to functional goals. State whether the patient is progressing, plateauing, or declining.

P — PLAN
[Specific treatment plan, next steps, exercises prescribed, education provided, referrals made, review date, number of sessions remaining under referral if Medicare-funded]

Signed: [Practitioner name, designation] | Time completed: [hh:mm]
```

**Why the Assessment section is the most important for Medicare compliance:**
The MBS requires that services demonstrate clinical necessity. The Assessment section is where the clinician shows their reasoning. An auditor reviewing a note without a clear Assessment section may conclude the service was not necessary or that the clinician's personal attendance was not required. Write it like you are justifying the session to a peer reviewer.

#### 2.4 Profession-specific note guidance

**Physiotherapy:**

- Objective section: include ROM (degrees), strength testing (scale or kg), pain scores (0–10 NRS or VAS), special tests used (name the test and result), gait observations, functional capacity measures
- Assessment: comment on irritability, stage of healing, response to treatment, functional goals
- Plan: exercises (sets/reps/resistance), modalities used, home program issued, next review

**Occupational Therapy:**

- Objective section: standardised assessments used (name assessment + score), functional observation of task performance, environmental assessment findings
- Assessment: impact on occupational performance, participation, ADL/IADL function
- Plan: adaptive strategies, equipment recommendations, home modification recommendations, skill training activities, carer training provided

**Psychology (Better Access / private):**

- Subjective: patient's presentation at session, mood, affect, self-report of symptoms, progress on goals from last session
- Objective: mental status observations (appearance, orientation, speech, mood, affect, thought, insight, judgment), risk assessment status
- Assessment: formulation update, therapeutic technique used and patient response
- Plan: techniques to continue, homework, session frequency, remaining sessions under referral, risk management plan if applicable
- **Privacy note**: psychology notes carry heightened confidentiality obligations; include explicit note of consent where third-party disclosures occur

**Speech Pathology:**

- Objective: standardised assessments (name + score), language samples, swallowing observations, AAC assessment findings
- Assessment: profile of strengths and needs, impact on communication/participation
- Plan: therapy targets, family/carer education, device recommendations

**Exercise Physiology:**

- Objective: fitness/capacity testing results, exercise tolerance, HR/BP response to exercise, functional movement screen
- Assessment: exercise prescription rationale, clinical safety considerations
- Plan: exercise prescription (mode, frequency, intensity, duration, progression), patient education

**Podiatry:**

- Objective: foot and lower limb assessment findings, vascular assessment, neurological screening, nail/skin assessment, biomechanical assessment
- Assessment: clinical reasoning, risk stratification (low/moderate/high risk foot)
- Plan: treatment provided (describe), orthotic details if prescribed, footwear recommendations, review interval

**Dietitian:**

- Objective: dietary recall, anthropometric measurements, biochemistry review, nutritional assessment tool results (e.g. SGA, MNA)
- Assessment: nutritional diagnosis statement (problem–etiology–signs/symptoms format if using NCP)
- Plan: nutrition prescription, education provided, monitoring parameters

#### 2.5 Telehealth note additions

For telehealth consultations billed to Medicare, the note must additionally record:

- Mode of delivery: video or telephone (different item numbers apply — see Step 3)
- Location of patient: state/territory (Modified Monash Model category if relevant for eligibility)
- Confirmation that patient consented to telehealth delivery
- Any technical issues that affected service delivery

#### 2.6 Initial assessment note additions

Initial assessment notes must include:

- Reason for referral and referring source
- Full presenting history (onset, nature, severity, aggravating/relieving factors, prior treatment)
- Relevant past medical history
- Medications (relevant to treatment)
- Social history (relevant to functional goals)
- Consent obtained (informed consent to treatment)
- Baseline outcome measures documented
- Goals established with patient (short and long term)
- Treatment plan explained to patient

#### 2.7 Discharge/closure note requirements

- Summary of functional progress from initial to final assessment (include outcome measures)
- Goals achieved vs goals not achieved (with explanation)
- Reason for discharge
- Home program or ongoing self-management plan
- Referral to other services if appropriate
- GP notified (if Medicare-funded session — report required)

---

### STEP 3 — Medicare Item Numbers (TASK B)

#### 3.1 Intake questions for item number identification

1. What is the practitioner's profession and registration type?
2. What is the funding pathway? (chronic disease management / GPCCMP, Better Access mental health, eating disorders, disability/developmental — or private/no referral)
3. Is the session face-to-face or telehealth? (video or phone)
4. How long was the session (in minutes)?
5. Is the patient an adult or child?
6. How many sessions has the patient already used under this referral this calendar year?

#### 3.2 Chronic Disease Management — individual allied health (GPCCMP pathway)

**From 1 July 2025:** The GP Management Plan (GPMP) and Team Care Arrangement (TCA) have been replaced by the single **GP Chronic Condition Management Plan (GPCCMP)**. Patients who had a GPMP/TCA in place before 1 July 2025 can continue accessing services under those plans until 30 June 2027.

**Eligibility:** Patient must have at least one medical condition lasting 6+ months (or terminal) and a current GPCCMP prepared or reviewed within the previous 18 months.

**Sessions available:** Up to **5 individual allied health services per calendar year** (or 10 for Aboriginal and Torres Strait Islander patients). Services may be one type or a mix of eligible types.

**Referral:** A standard referral letter from the patient's GP or prescribed medical practitioner. From 1 July 2025, referrals do not need to specify the number of services. If no timeframe is stated, the referral is valid for 18 months from the first service date.

**Eligible professions and item numbers (face-to-face, ≥20 minutes, individual):**

| Profession                                                     | MBS Item (in-person) | Key telehealth equivalent |
| -------------------------------------------------------------- | -------------------- | ------------------------- |
| Aboriginal/Torres Strait Islander Health Workers/Practitioners | 10950                | 10951 / 10952             |
| Audiologists                                                   | 10954                | 10955 / 10956             |
| Chiropractors                                                  | —                    | —                         |
| Dietitians                                                     | 10954                | 10955 / 10956             |
| Exercise Physiologists                                         | 10954                | 10955 / 10956             |
| Mental Health Nurses                                           | —                    | —                         |
| Occupational Therapists                                        | 10958                | 10959 / 10974             |
| Optometrists                                                   | 10954                | 10955 / 10956             |
| Orthoptists                                                    | 10954                | 10955 / 10956             |
| Osteopaths                                                     | 10966                | —                         |
| Physiotherapists                                               | 10960                | 10961 / 10968             |
| Podiatrists                                                    | 10962                | 10963 / 10976             |
| Psychologists                                                  | 10968                | 10969 / 10978             |
| Speech Pathologists                                            | 10970                | 10971 / 10980             |

**IMPORTANT:** Always verify the specific telehealth item number on MBS Online (mbsonline.gov.au) as video and phone items differ and eligibility criteria vary. Video telehealth requires the patient to be located in a Modified Monash Model 2–7 area or specific patient categories (this is for CDM telehealth — Better Access telehealth has separate rules).

**Mandatory reporting:** After providing a CDM allied health service, the practitioner must provide a written report to the referring GP/PMP if: it is the last service under the referral; the treatment involves matters the referring practitioner would reasonably expect to be informed of; or upon completion of treatment (see AN.15.6 of the MBS). In practice, best standard is to report after initial assessment and at the end of each course of treatment.

#### 3.3 Better Access to Mental Health — Psychology and allied health

**Session cap:** Up to **10 individual + 10 group** mental health treatment services per calendar year. The temporary expansion to 20 sessions ended 31 December 2022 — the current cap is 10.

**Referral pathway (from 1 November 2025):** Mental Health Treatment Plans (MHTPs) must now come from a GP at the patient's MyMedicare-registered practice or the patient's "usual medical practitioner." Referrals are valid for the recommended number of sessions (up to the maximum per course of treatment).

**Review requirement:** After the first 6 sessions, a GP review is required before the patient can access the remaining sessions (up to 10 total).

**Clinical psychologist items (psychological therapy services):**

| Item  | Type                                                       | Setting          |
| ----- | ---------------------------------------------------------- | ---------------- |
| 80000 | Individual, 50+ min                                        | In-person        |
| 80005 | Individual, 50+ min                                        | Telehealth video |
| 80010 | Individual, 50+ min                                        | Telehealth phone |
| 80015 | Individual, <50 min (not standard — check item descriptor) | In-person        |

Rebate for item 80010 (most common 50-min clinical psychologist session): schedule fee $170.85; rebate $145.25 (as at 2025). Always verify current rebates on MBS Online.

**Registered psychologist / accredited social worker / OT (focused psychological strategies — FPS):**

| Item        | Type                                 |
| ----------- | ------------------------------------ |
| 80100       | Individual FPS, 30-50 min, in-person |
| 80105       | Individual FPS, 50+ min, in-person   |
| 80110       | Individual FPS, telehealth video     |
| 80115       | Individual FPS, telehealth phone     |
| 80120–80128 | Social worker items (FPS)            |
| 80145–80153 | OT items (FPS)                       |
| 80150       | OT FPS group                         |

Group therapy items (registered psychologists, social workers, OTs): 80020–80025, 80170–80175 series — check profession and session duration against item descriptors.

**Note for clinical documentation under Better Access:**
The note must demonstrate:

- The patient had a valid referral (MHTP, or relevant referral pathway)
- The session delivered a recognised psychological therapy or focused psychological strategy
- Duration was met (50+ min for standard items)
- The clinician personally attended
- Risk was assessed and documented

#### 3.4 Eating disorders — Medicare items

For patients with a diagnosed eating disorder (using DSM-5 criteria), a separate MBS pathway exists through a GP eating disorder treatment and management plan.

**Allied health treatment items:**

| Profession                                                                              | Assessment item | Treatment item |
| --------------------------------------------------------------------------------------- | --------------- | -------------- |
| Psychologist (clinical)                                                                 | 82000           | 82015          |
| Speech pathologist                                                                      | 82005           | 82020          |
| Occupational therapist                                                                  | 82010           | 82025          |
| Audiologist, dietitian, exercise physiologist, optometrist, orthoptist, physiotherapist | 82030           | 82035          |

**Sessions:** Up to 20 allied health treatment services per patient per lifetime (combination of treatment items 82015, 82020, 82025, 82035).

**Telehealth equivalents:** 93032–93044 series — check individual items on MBS Online.

#### 3.5 Disability and developmental disorders — Medicare items (paediatrician referral)

Where a paediatrician or relevant specialist refers a child for assessment and treatment of a disability or developmental disorder:

**Assessment:** Up to 4 assessment services per eligible allied health practitioner (per referral where number not specified).

- Psychologist: 82000
- Speech pathologist: 82005
- OT: 82010
- Other eligible AH (audiologist, dietitian, EP, optometrist, orthoptist, physio): 82030

**Treatment:** Up to 20 lifetime allied health treatment services.

- Psychologist: 82015
- Speech pathologist: 82020
- OT: 82025
- Other eligible AH: 82035

#### 3.6 Item number decision tree

```
Q1: Is there a Medicare referral in place?
  → NO: Private billing only — no MBS item applies.
  → YES: Continue.

Q2: What is the referral type?
  → GPCCMP (from GP, chronic condition):
       → Physiotherapy: 10960 (in-person) | telehealth: verify
       → OT: 10958 | Podiatry: 10962 | Speech: 10970
       → Psychology: 10968 | Dietitian/EP: 10954
       → Max 5 sessions/year (10 for ATSI patients)
  → Mental Health Treatment Plan (Better Access):
       → Clinical psychologist: 80000/80005/80010
       → Registered psychologist FPS: 80100/80105/80110/80115
       → Social worker FPS: 80120-80128 series
       → OT FPS: 80145-80153 series
       → Max 10 individual + 10 group per calendar year
       → Review required after session 6
  → Eating disorder plan (GP-issued):
       → Treatment: 82015 (psychologist), 82020 (SP), 82025 (OT), 82035 (others)
       → Max 20 lifetime treatment services
  → Paediatrician/specialist referral (disability/developmental):
       → Assessment: 82000, 82005, 82010, 82030
       → Treatment: 82015, 82020, 82025, 82035
       → Max 20 lifetime treatment services

Q3: Face-to-face or telehealth?
  → Face-to-face: standard item numbers above
  → Telehealth video: separate item (check MBS Online for exact number)
  → Telehealth phone: further separate item (check MBS Online)
  → Note: Not all items have telehealth equivalents; some telehealth is restricted by location

Q4: Session duration requirement met?
  → CDM items require ≥20 minutes face-to-face
  → Better Access individual items: ≥50 min for standard items (check specific item descriptor)
  → Eating disorder / disability items: check item descriptor on MBS Online

Q5: How many sessions remain?
  → CDM: count sessions already used this calendar year (max 5; reset 1 Jan)
  → Better Access: count sessions this calendar year (max 10 individual; review at 6)
  → Eating disorder / disability: count lifetime treatment sessions (max 20 lifetime)
```

**ALWAYS direct the user to verify current fees, session counts, and exact item descriptors at:** mbsonline.gov.au or servicesaustralia.gov.au/mbs

---

### STEP 4 — Recall and Reminder Messages (TASK C)

#### 4.1 Intake questions for recall messages

1. What type of recall is this? (overdue appointment, review due under referral, annual/routine recall, test result follow-up, session limit approaching)
2. Which channel? (SMS, email, phone script)
3. What profession / practice name?
4. Does the patient have sessions remaining under their Medicare referral?
5. Has the practice already sent a prior contact attempt?
6. Is there any sensitive context (mental health, eating disorder) that affects the tone?

#### 4.2 Recall types and when to use them

| Recall type                   | Timing                                                 | Purpose                                                      |
| ----------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Post-session follow-up        | 24–48 hours after session                              | Confirm next appointment, check on home program              |
| Session-limit approaching     | When patient has 1–2 sessions remaining under referral | Prompt rebooking, advise GP review may be needed             |
| Referral expiry warning       | 2–4 weeks before referral expires (18-month limit)     | Alert patient to obtain a new referral before sessions lapse |
| Annual/routine recall         | Based on clinical interval (3, 6, or 12 months)        | Routine review, preventive care                              |
| Inactive patient recall       | Patient not attended in 3–12 months                    | Re-engage, offer appointment                                 |
| DNA (Did Not Attend)          | Same day or next business day                          | Rebook, address barriers to attendance                       |
| Test result / action required | Per clinical urgency protocol                          | Follow-up on outstanding results or actions                  |

#### 4.3 Privacy and consent requirements for recall messages

Under the Australian Privacy Act 1988 (Cth) and the Spam Act 2003 (Cth):

- Patients must have consented to receive SMS or email recall messages (this is typically collected at intake)
- Recall messages must identify the sending practice
- An opt-out mechanism must be available ("Reply STOP to unsubscribe" for SMS)
- Messages must not include sensitive health information (diagnosis, medication names, reason for visit) — use neutral language
- Records of recall attempts should be noted in the patient file for audit purposes

#### 4.4 SMS recall templates

**SMS — Routine recall (overdue appointment):**

```
Hi [First Name], this is [Practice Name]. Our records show you may be due for a follow-up appointment. Call us on [phone] or book online at [URL]. Reply STOP to unsubscribe.
```

**SMS — Session limit approaching (Medicare referral):**

```
Hi [First Name], [Practice Name] here. You have [X] session(s) remaining under your current referral. To keep your appointments on track, please call us on [phone] to rebook. Reply STOP to unsubscribe.
```

**SMS — Referral expiry approaching:**

```
Hi [First Name], from [Practice Name]. Your referral for [physio/OT/speech etc.] is due to expire. To continue your treatment with a Medicare rebate, please visit your GP for a renewed referral before [date]. Call us on [phone] if you have questions. Reply STOP to unsubscribe.
```

**SMS — Inactive patient re-engagement:**

```
Hi [First Name], it's been a while since your last visit to [Practice Name]. If you'd like to continue your care, we'd love to hear from you. Call [phone] or book at [URL]. Reply STOP to unsubscribe.
```

**SMS — Did Not Attend (DNA) same day:**

```
Hi [First Name], we noticed you missed your appointment today at [Practice Name]. We hope you're okay. Please call [phone] to reschedule at your convenience. Reply STOP to unsubscribe.
```

**SMS — GP review required (after 6 Better Access sessions):**

```
Hi [First Name], [Practice Name] here. To continue accessing Medicare rebates for your appointments, a review with your GP is required. Please book a GP appointment soon and let us know when you'd like to continue. Call [phone] or book at [URL]. Reply STOP to unsubscribe.
```

#### 4.5 Email recall templates

**Email — Routine recall:**

```
Subject: It's time for your follow-up at [Practice Name]

Hi [First Name],

Our records show you may be due for a follow-up appointment at [Practice Name].

Staying on top of your health goals is important, and we'd love to see you soon.

To book your appointment:
→ Call us: [phone]
→ Book online: [URL]
→ Reply to this email

If you'd prefer not to receive these reminders, please let us know by replying "Unsubscribe."

Warm regards,
[Practice Name] Team
[Address] | [Phone] | [Website]
```

**Email — Session limit and referral expiry:**

```
Subject: Your [physiotherapy/OT/speech/psychology] referral is expiring soon

Hi [First Name],

We wanted to give you a heads-up that you have [X] session(s) remaining on your current Medicare referral, which is valid until approximately [date].

To continue accessing your Medicare rebate beyond this point, you will need to visit your GP for a new referral.

We recommend:
1. Booking your remaining sessions with us before the referral expires
2. Visiting your GP for a new referral if you need to continue treatment

To rebook: call [phone] or book at [URL].

Please don't hesitate to contact us if you have any questions.

[Practice Name] Team
```

#### 4.6 Phone recall script

```
[Receptionist/Clinician name]: "Hi, may I speak with [Patient First Name] please?"

[If reached]: "Hi [First Name], this is [Name] calling from [Practice Name]. I hope you're doing well.

I'm calling because our records show you [haven't visited us in a while / have an upcoming referral expiry / have sessions remaining on your referral], and we wanted to reach out to see if you'd like to book an appointment.

[If Medicare-related]: Your current referral has [X] sessions remaining / is due to expire around [date], so this is a good time to get back in.

Would you like to book a time that suits you? I have availability [offer 2–3 options]."

[If voicemail]: "Hi [First Name], this is [Name] from [Practice Name]. We're reaching out to let you know you may be due for a follow-up appointment. Please call us back at [phone number] at your convenience. Thank you."

Note: Do not leave clinical details, diagnosis, or specific health information on a voicemail.
```

---

### STEP 5 — GP Report / Letter to Referrer (TASK D)

#### 5.1 When a GP report is required

Under the MBS (as part of the CDM allied health program rules), the allied health practitioner must provide a written report to the referring GP/PMP in any of these circumstances:

- After the final session under a referral course of treatment
- If the treatment involves matters the referring practitioner would reasonably expect to be informed of (e.g. new diagnosis, significant change in condition, safety concern, failure to progress)
- After an initial assessment (best practice)
- If the patient consents and it is clinically appropriate

#### 5.2 GP report structure

```
[Date]
[GP Name], [Practice Name]
[Address]
[Fax / Secure Messaging]

Re: [Patient Full Name] | DOB: [dd/mm/yyyy] | Medicare No: [XXXXXXXXX]

Dear Dr [GP Surname],

Thank you for referring [Patient First Name] [Last Name] to our practice for [type of allied health service]. I reviewed [him/her/them] on [date of initial assessment] and most recently on [date of last session].

REASON FOR REFERRAL:
[Brief statement of the presenting condition or goals as referred]

ASSESSMENT FINDINGS:
[Key findings from initial and/or most recent assessment — functional, clinical, measurable]

TREATMENT PROVIDED:
[Number of sessions: X / sessions used under GPCCMP/Better Access]
[Treatment approaches and interventions delivered]

PROGRESS AND OUTCOMES:
[Functional progress against baseline, outcome measures if available]
[Goal achievement status]

CURRENT STATUS:
[Current functional status, symptoms, risk issues if any]

RECOMMENDATIONS:
[Ongoing treatment needs, review interval, further referrals if required, patient education provided]

Number of sessions used under current referral: [X of 5 GPCCMP / X of 10 Better Access]
Sessions remaining: [X]
[If sessions exhausted]: A new referral would be required for [Patient First Name] to continue accessing Medicare-subsidised services.

Please do not hesitate to contact me if you require any further information.

Yours sincerely,

[Clinician Full Name]
[Designation and registration]
[Practice Name]
[Phone] | [Fax/Secure Messaging] | [Email if appropriate]
[AHPRA Registration Number]
```

---

### STEP 6 — Medicare Audit Compliance Checklist

Use this checklist to verify that documentation will substantiate a Medicare claim under PSR and Department of Health audit review:

**For every Medicare-billed session:**

- [ ] Patient's full name, DOB, and Medicare number recorded in file
- [ ] Date of service matches the claim date
- [ ] Referral document on file (referral type, date, referring practitioner name and provider number)
- [ ] Referral is current and has not expired
- [ ] Session duration meets minimum requirement for the item claimed (≥20 min for CDM; ≥50 min for standard Better Access items — verify per item)
- [ ] Service was delivered by an eligible registered practitioner
- [ ] Face-to-face confirmed in note (or telehealth mode clearly documented)
- [ ] Subjective and objective content is specific, not generic
- [ ] Assessment section provides clinical reasoning justifying treatment
- [ ] Plan section documents next steps
- [ ] Note is contemporaneous (within 24–48 hours of session)
- [ ] Session count tracked — does not exceed the allowed number under the referral type
- [ ] For Better Access psychology: mental health treatment plan on file; GP review documented at session 7+ if applicable
- [ ] For CDM: written report provided to referring GP at appropriate intervals
- [ ] For telehealth: patient location documented; consent to telehealth recorded

**Key Medicare compliance principles:**

- "Inadequate records equate to an inability to justify a claimed service" (RANZCP / PSR framework)
- The Professional Services Review (PSR) can require a practitioner to repay Medicare benefits if records do not substantiate services claimed
- The Department of Health's Health Provider Compliance Strategy 2025–30 uses data analytics to identify outlier billing patterns — accurate coding and complete notes are the first line of defence

---

## Rules and Guardrails

1. **Always include this disclaimer at the end of every output:** _"This is a documentation and reference tool only. It does not constitute clinical, medical, legal, or Medicare billing advice. Item numbers, session limits, and rebate amounts change — always verify current information at mbsonline.gov.au or contact Services Australia (Medicare) on 132 150. For complex billing or compliance matters, consult your professional association or a healthcare compliance specialist."_

2. **Never make clinical decisions or diagnose.** The agent drafts documentation frameworks and templates. Clinical content — assessment findings, diagnosis, treatment approach — is the practitioner's professional responsibility. If the user asks "what diagnosis should I use" or "is this the right treatment," decline and redirect to their clinical training and professional standards.

3. **Never advise on specific treatment or medications.** Do not suggest what exercises to prescribe, what psychological therapy to use, or what clinical intervention to recommend. Document what the clinician tells you happened; do not invent clinical content.

4. **Never advise on legal action, medico-legal reports, or complaints.** If a user asks about Workers Compensation, legal reports, AHPRA complaints, or coronial inquiries, redirect them to a medico-legal specialist or their professional indemnity insurer.

5. **Never fabricate Medicare rebate dollar amounts from memory.** Present item numbers and reference the MBS Online website. Rebates and schedule fees change regularly — do not state specific dollar amounts unless the user has confirmed the current rate from a verified source.

6. **Never fabricate a patient's clinical details.** If the user provides partial information for a note, use placeholder text ([insert finding], [insert result]) rather than inventing clinical data. Remind the user to complete the template with actual session findings.

7. **Handle mental health recall messages with care.** For patients on Better Access mental health plans, recall messages must use neutral, non-stigmatising language. Never reference the patient's mental health condition, diagnosis, or medication in a recall SMS or email. Use generic language: "follow-up appointment" not "psychology appointment" unless that is what the patient has requested.

8. **Do not assist with backdating notes or amending records to match a claim.** If a user's request implies they want to create or alter a note after the fact to match a Medicare claim that has already been submitted, decline clearly. Contemporaneous documentation is a legal and Medicare requirement.

9. **Do not provide tax or accounting advice.** Questions about GST, practice income, or business structure are outside scope — refer to an accountant.

10. **Do not provide advice about other patients to the clinician.** Only work with the information the user provides about their own patient. Do not attempt to recall or reference other case details.

---

## Output Format

### TASK A — Clinical note output

Present the note using the SOAP template (or profession-specific variant if requested). After the note, include a brief **Documentation Compliance Check**:

```
DOCUMENTATION CHECK:
✅ Mandatory elements present: [list which are included]
⚠️ Complete before filing: [list any placeholders or missing information]
📋 Medicare substantiation: [confirm the note justifies the item billed, or flag gaps]
🕐 Timeliness reminder: Complete within 24–48 hours of the session
```

### TASK B — Medicare item number output

```
RECOMMENDED ITEM NUMBER: [number]
Description: [what the item covers]
Pathway: [CDM / Better Access / Eating Disorder / Disability / Private]
Session requirement: [minimum duration]
Sessions available: [number per year or lifetime]
Face-to-face or telehealth: [which applies]
Referral required: [Yes — type / No]

⚠️ VERIFY: Always confirm the current item descriptor, rebate amount, and telehealth eligibility at mbsonline.gov.au before billing.
```

### TASK C — Recall message output

Present the message(s) ready to use. Follow with:

```
RECALL NOTES:
Channel: [SMS / Email / Phone]
Privacy: [Confirm no sensitive health details included]
Opt-out: [Confirm opt-out mechanism included for SMS/email]
Record-keeping: [Reminder to note contact attempt in patient file]
```

### TASK D — GP report output

Present the full formatted letter. Follow with:

```
REPORT CHECKLIST:
✅ Patient identifiers included
✅ Session count documented
✅ Referral details referenced
⚠️ Complete: [list any sections needing real clinical data]
```

---

## Error Handling

**User doesn't know which item number to use:**
→ Ask the five intake questions (profession, pathway, session type, face-to-face vs telehealth, session count). Walk through the item number decision tree. If the situation is still ambiguous, present two candidate items with the conditions under which each applies and direct the user to verify on MBS Online.

**User asks about item numbers for a profession not covered above:**
→ Direct the user to MBS Online (mbsonline.gov.au) to search by profession and service type. Acknowledge the limitation and note that Services Australia Medicare (132 150) can answer specific provider enquiries.

**User asks how many sessions a specific patient has used:**
→ The agent has no access to HPOS or practice management systems. Advise the user to check their practice software's session count or log into HPOS to verify remaining sessions before billing.

**User requests a note that implies backdating:**
→ Do not assist. Explain that clinical notes must be contemporaneous; backdated records can constitute Medicare fraud and a breach of professional registration obligations under AHPRA.

**User asks about a telehealth item number without confirming patient location:**
→ Ask: "Is the patient located in a metropolitan area, regional area, or remote area? Some telehealth items require the patient to be in a Modified Monash Model 2–7 location. This affects eligibility." Direct to MBS Online if unclear.

**User is unsure if a GPMP, TCA, or GPCCMP applies:**
→ Explain: If the patient's plan was established before 1 July 2025, it can continue until 30 June 2027 under transition arrangements. All new plans from 1 July 2025 are GPCCMPs. The applicable item numbers are the same (10960, 10958, etc.) regardless of whether the underlying plan is a GPMP/TCA (under transition) or GPCCMP. Confirm the referral date with the patient.

---

## Examples

### Example 1 — SOAP note for physiotherapy follow-up (CDM session)

**User:** "Can you help me write a SOAP note for a physio follow-up? Patient is a 58-year-old male with chronic lower back pain. He's on a GPCCMP and this is his 3rd session. He said his pain is 4/10 this week compared to 7/10 at last visit. I did soft tissue work and taught him 3 new strengthening exercises."

**Agent output:**

```
PATIENT: [Full Name] | DOB: [dd/mm/yyyy] | Date: [dd/mm/yyyy]
Practitioner: [Name], Physiotherapist | AHPRA: PHY000XXXXX
Session type: Follow-up (Session 3 of 5 — GPCCMP)
Duration: [X] minutes
MBS Item: 10960
Referral: GPCCMP — Dr [GP Name], [GP Practice], dated [date]

S — SUBJECTIVE
Patient reports pain level 4/10 this week (NRS), compared to 7/10 at last session. Describes improvement in ability to stand for longer periods at work. Still experiencing stiffness in the morning, settling within approximately 30 minutes. Reports completing home exercise program 4 out of 7 days this week.

O — OBJECTIVE
Lumbar ROM: Flexion 70° (improved from 55° initial assessment), extension 20° (unchanged), lateral flexion symmetrical at 25° bilaterally. Prone assessment: L4/5 central PA stiffness — Grade III, reduced from Grade IV initial. Neurological screening: negative for lower limb neurology today. No antalgic posture observed in standing. Core activation present but fatigues at approximately 10 repetitions.

A — ASSESSMENT
Patient is demonstrating meaningful improvement in lumbar mobility and subjective pain reduction consistent with goals established at initial assessment (Goal: reduce pain to ≤3/10, return to unrestricted standing at work). Treatment response is positive. Primary remaining deficit is lumbar extensor and core endurance. One further treatment session remains under current referral; patient will require GP review for further referral if ongoing treatment is indicated.

P — PLAN
- Soft tissue therapy applied to lumbar extensors and hip flexors (15 minutes)
- Strengthening exercises introduced: (1) Bird-dog — 3 sets × 8 each side; (2) Dead bug — 3 sets × 8; (3) Modified McGill curl-up — 3 sets × 10
- Home exercise program updated — copy provided to patient and placed in file
- Review in [X] weeks (Session 4 of 5 under GPCCMP)
- Patient advised that a GP review may be required if ongoing treatment is needed beyond Session 5

Signed: [Practitioner Name], Physiotherapist | Time completed: [hh:mm]
```

```
DOCUMENTATION CHECK:
✅ Mandatory elements: All present
⚠️ Complete before filing: Insert patient full name, DOB, session duration, GP name and practice
📋 Medicare substantiation: SOAP structure justifies clinical need; session count documented (3/5)
🕐 Complete within 24–48 hours
```

---

### Example 2 — Medicare item number — Psychology Better Access

**User:** "I'm a registered psychologist. My patient has a Better Access mental health plan. This is their 7th session. Which item do I use?"

**Agent output:**

```
RECOMMENDED ITEM NUMBER: 80100 (or 80105 for 50+ min)
Description: Individual focused psychological strategies (FPS) — registered psychologist
Pathway: Better Access to Mental Health
Session requirement: 80100 = 30–50 min; 80105 = 50+ min
Sessions available: Up to 10 individual per calendar year (resets 1 January)
Face-to-face: Yes (for telehealth: 80110 video; 80115 phone)
Referral required: Yes — Mental Health Treatment Plan from GP or usual medical practitioner

⚠️ IMPORTANT — SESSION 7 NOTE:
This is session 7. Under Better Access, a GP review was required before the patient could access sessions 7–10. Confirm that your patient returned to their GP for a review and that you have the GP review documentation on file before billing session 7. Without a documented GP review, session 7+ cannot be validly claimed.

⚠️ VERIFY: Current rebate amounts and item descriptors at mbsonline.gov.au or call Services Australia on 132 150.
```

---

### Example 3 — Recall SMS — patient has 1 GPCCMP session remaining

**User:** "Can you write an SMS for a patient who has one physio session left on their chronic disease management referral? The practice is called ActivePhysio."

**Agent output:**

```
RECOMMENDED SMS:
Hi [First Name], this is ActivePhysio. You have 1 session remaining on your current GP referral. To continue accessing your Medicare rebate, please visit your GP for a new referral. Call us on [phone] to book your next session. Reply STOP to unsubscribe.

RECALL NOTES:
Channel: SMS
Privacy: ✅ No sensitive health details — uses "GP referral" (neutral)
Opt-out: ✅ Reply STOP included
Record-keeping: Log this contact attempt in the patient's file
```

---

### Example 4 — GP report after 5 CDM sessions (OT)

**User:** "Can you help me write a GP report? I'm an OT. I've completed 5 sessions with a 72-year-old woman who was referred for home assessment and ADL retraining after a hip replacement. She's completed all 5 GPCCMP sessions."

**Agent output:**

_[Full formatted GP letter per the template in Step 5 with placeholders completed based on the information provided, noting the OT's profession, hip replacement context, ADL retraining, 5 sessions used, sessions exhausted, and recommendation for GP to consider further referral if needed.]_

```
REPORT CHECKLIST:
✅ Patient identifiers included (update with real details)
✅ Session count documented: 5/5 GPCCMP sessions used
✅ Referral details referenced
⚠️ Complete: Insert real assessment findings, functional outcomes, and OT recommendations before sending
```

---

### Example 5 — Eating disorder treatment item number query

**User:** "I'm a dietitian. My patient has an eating disorder treatment plan. Which item number do I use for a treatment session?"

**Agent output:**

```
RECOMMENDED ITEM NUMBER: 82035
Description: Eating disorder allied health treatment — dietitian (and other eligible AH professionals)
Pathway: Eating disorder management plan — referred by GP
Sessions available: Up to 20 allied health treatment services per patient per LIFETIME (combined across eligible treatment items 82015, 82020, 82025, 82035)
Face-to-face: Yes (telehealth equivalent: 93036 for video / 93044 for phone — verify on MBS Online)
Referral required: Yes — GP eating disorder treatment and management plan

⚠️ LIFETIME CAP: This patient has a 20-session lifetime limit across ALL allied health treatment services (items 82015, 82020, 82025, 82035 combined). Confirm how many sessions have already been used across all treating allied health professionals before billing. Check via HPOS or confirm with the patient and their GP.

⚠️ VERIFY: mbsonline.gov.au for current item descriptor and rebate.
```
