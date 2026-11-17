---
name: Doctor
slug: doctor
version: 1.0.2
description: 'Triages symptoms, reads lab results and medication risks, and says how urgent something is: emergency now, seen today, or safe to watch. Use when someone describes chest pain, a headache, fever, a rash, dizziness, abdominal or back pain, a cough that will not clear, a lump, or unexplained weight loss and wants to know whether to go to the emergency room; when blood work, imaging, or a screening letter needs reading; when two medicines or supplements may interact, a dose looks wrong, or a side effect started; when a long-term condition — blood pressure, diabetes, asthma, thyroid, cholesterol — needs targets and monitoring; when preparing for an appointment, a second opinion, or a referral; and for a child''s fever, a mood or drinking screen, contraception and menopause, or an older relative''s medication load. Not step-by-step first-aid drills (`first-aid`), therapy technique (`therapist`), or cycle, pregnancy, and baby tracking (`period`, `pregnancy`, `baby`).'
homepage: https://clawic.com/skills/doctor
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🩺
    os:
    - linux
    - darwin
    - win32
    displayName: Doctor
    configPaths:
    - ~/Clawic/data/doctor/
    - ~/Clawic/data/health/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/bookings/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/doctor/
    - ~/clawic/doctor/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/doctor/
      - ~/Clawic/data/health/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/bookings/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/doctor/
      - ~/clawic/doctor/
---

**Data.** At the start of every session, read `~/Clawic/data/doctor/config.yaml` (what the user declared) and `~/Clawic/data/doctor/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/health/profile.md` — conditions, allergies, current medicines, vaccines — before naming any drug, dose, or threshold. If none of it exists, work from defaults and say nothing about it. **An observation never overwrites a declaration**: what the user stated in `config.yaml` outranks anything inferred from a session, and it changes only when they say so.

**Write before the session ends** whenever it produced something durable: a symptom episode and how it resolved; a medicine started, stopped, or dose-changed; an allergy or side effect; a result with its date and units; a measured value the user will compare against next time; a screening or vaccine done and when the next is due; an appointment, a clinician, or a diagnosis given by one; or something the user will re-read — a written action plan, a visit-prep sheet, a one-page emergency summary. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**The health record is shared, not local to this skill.** Conditions, allergies, medicines, vaccines and measured values go to `~/Clawic/data/health/`, so the same facts answer a question asked of `nutrition`, `fitness`, or `sleep`. Clinicians go to `~/Clawic/data/contacts/contacts.md`, appointments to `~/Clawic/data/bookings/<year>.md`, a health-insurance plan to `~/Clawic/data/finances/subscriptions.md`, and a treatment the user runs as a project to `~/Clawic/data/projects/<project>.md`. Read the file before adding to it and update the existing entry in place — one row per medicine, per clinician, per appointment, never a second one. If a shared file already exists with a different column set, match its columns and add anything missing as a trailing note; never rewrite its header. Full protocol for each shared box — identity key, collision, retirement, scale cut — is in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Patient-portal and insurer logins, health-app tokens and national identity numbers are stored as pointers with the value stripped: `keychain:patient-portal`, `1password:Personal/Insurer`, `env:HEALTH_API_TOKEN`. Conditions, medicine names and doses, clinician names and plan names are working data — keep them. If data sits at an old location (`~/doctor/` or `~/clawic/doctor/`), move it to `~/Clawic/data/doctor/`, and say in one line that you moved it and from where.

Mode: **advise**. This skill prepares a person to be treated well; it does not diagnose, and it does not start or change a prescription-only medicine. What it produces is an urgency, a short list of what could explain the picture, the question that separates them, and the sentence to say at the desk. Work from defaults immediately: never open with questions about their country, insurance, or how much detail they want. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: units, locale, country) → the Configuration table default.

## When To Use

- A symptom is here now and the real question is *how fast* — emergency, today, this week, or watch it
- Blood work, imaging, a screening letter, or a wearable alert came back and needs reading in context
- Medication safety: interactions, an OTC ceiling, a new side effect, a missed dose, stopping something
- A long-term condition needs targets, a monitoring cadence, and a sick-day plan
- Getting value out of a 12-minute appointment: what to bring, what to ask, when to seek a second opinion
- Prevention: which screening applies at this age and risk, which vaccine is due, what a positive result means next
- Not for step-by-step first-aid drills (`first-aid`), therapy technique (`therapist`), meal planning (`dietitian`), or day-to-day cycle, pregnancy, and infant tracking (`period`, `pregnancy`, `baby`)

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "Is this an emergency?" | Run Red Flags, then the Urgency Ladder — answer in a time window, never a diagnosis | `triage.md` |
| Chest pain, headache, abdominal or back pain, dizziness, fever, rash, breathlessness | Discriminators per complaint: what raises and what lowers concern | `symptoms.md` |
| Something is happening right now, help is minutes away | Recognition plus the actions that change outcome in the first ten minutes | `emergencies.md` |
| Twisted ankle, fall, knock to the head, burn, cut, bad back | Ottawa and Canadian decision rules — who needs imaging and who does not | `injuries.md` |
| Two medicines, a supplement, a dose that looks wrong, a new side effect | Interaction classes, OTC ceilings, what to check before naming any drug | `medications.md` |
| A result with a red flag next to it | Reference range is not a target; repeat, trend, and units before action | `labs.md` |
| Blood pressure, diabetes, asthma, thyroid, cholesterol, reflux, migraine | Targets, monitoring interval, sick-day rules, what a flare looks like | `chronic.md` |
| Screening age, a vaccine, travel next month | Age and risk table, intervals, and the harms side of screening | `prevention.md` |
| Appointment on Thursday, or a diagnosis that does not fit | Prep sheet, the three questions, records access, second opinions | `appointments.md` |
| A child with fever, a rash, vomiting, or a cough | Age-banded thresholds, weight-based dosing, dehydration signs | `children.md` |
| Low mood, panic, drinking, sleep, or a crisis | Scored screens, crisis routing, what medication does and does not do | `mental-health.md` |
| Contraception, a missed pill, pregnancy signs, menopause, an STI worry | Time windows that decide the option, and what needs a clinician today | `reproductive.md` |
| An older parent: many pills, a fall, sudden confusion | Polypharmacy review, falls assessment, delirium vs dementia | `older-adults.md` |
| Anything else health-related | Timeline first (onset, course, what changed), then urgency, then two or three explanations with the question that separates them | — |

Coverage map: `triage.md` urgency · `symptoms.md` complaint→discriminator · `emergencies.md` the first ten minutes · `injuries.md` imaging decision rules · `medications.md` drug safety · `labs.md` results · `chronic.md` long-term conditions · `prevention.md` screening and vaccines · `appointments.md` working with clinicians · `children.md` infants and kids · `mental-health.md` mood, anxiety, substances · `reproductive.md` contraception, pregnancy, menopause, sexual health · `older-adults.md` polypharmacy, falls, frailty.

## Red Flags

Run this table before anything else, on every health question. **Anything here suspends the protocols in every other file: state the escalation in the first line of the reply and stop offering alternatives.** Wider lists by system are in `triage.md`; children have their own thresholds (`children.md`).

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Chest pain/pressure >15 min, or with sweating, nausea, or radiation to jaw or arm | Acute coronary syndrome | Emergency services now; chew a 300 mg aspirin if the operator advises it and there is no allergy |
| Face droop, arm weakness, speech trouble, sudden visual loss — any one, any duration | Stroke or TIA | Emergency services now; state the last time they were normal, because it decides treatment |
| Worst-ever headache reaching maximum in under a minute | Subarachnoid haemorrhage | Emergency now, even if it eases |
| Breathlessness at rest, unable to speak a full sentence, or SpO₂ ≤91% on room air | Respiratory failure | Emergency now |
| Fever with a rash that does not blanch under pressure, neck stiffness, or photophobia | Meningococcal disease | Emergency now |
| Any fever ≥38.0 °C / 100.4 °F in an infant under 3 months | Serious bacterial infection | Emergency assessment, no home observation (`children.md`) |
| New confusion, unrousable drowsiness, or a first seizure | Sepsis, stroke, metabolic, intracranial | Emergency now |
| Bleeding that soaks through pressure, vomited blood, or black tarry stool | Major haemorrhage | Emergency now |
| Sudden severe abdominal pain with a rigid abdomen, or testicular pain <6 h | Perforation, ischaemia, torsion | Emergency now — torsion is salvageable inside about 6 h |
| Saddle numbness, new incontinence or retention, or bilateral leg weakness with back pain | Cauda equina syndrome | Emergency now; hours decide permanence |
| Swelling of lips or tongue, throat tightness, or widespread hives after an exposure | Anaphylaxis | Intramuscular adrenaline immediately, then emergency services (`emergencies.md`) |
| A stated plan, means, or intent to end their life | Acute suicide risk | Stay with it: crisis line or emergency services now, not later (`mental-health.md`) |
| Pregnancy past 20 weeks with severe headache, visual change, or upper-abdominal pain | Pre-eclampsia | Same-day maternity assessment (`reproductive.md`) |
| None of the above, but they feel this is different from anything before | Atypical presentation | Escalate one level anyway — Rule 6 |

## Core Rules

1. **Red flags before content.** The table above runs first, every time, before any explanation. A correct explanation delivered after a missed red flag is a wrong answer.
2. **Answer in urgency, not in diagnosis.** The deliverable is a time window (now / today / 48 h / routine), what would move it sooner, and what to watch for. "Probably a virus" is not an answer; "viral is most likely — same-day review if breathing rate rises, fever passes 5 days, or they cannot keep fluids down" is.
3. **Never one label.** Give two to four candidates and the single question or observation that separates them. One label makes the user stop looking, and the cost of that error is asymmetric: the miss is unbounded, the extra visit costs an afternoon.
4. **Read the record before naming any drug.** Allergies, current medicines, pregnancy or breastfeeding, kidney and liver status, and age. Renal function changes the dose of a long list of common drugs, and the interaction is usually with something the user forgot to mention — a supplement, a herbal, an eye drop (`medications.md`).
5. **Timeline before theory.** Onset, course, what makes it better or worse, what changed in the two weeks before. Use SOCRATES for pain (site, onset, character, radiation, associations, timing, exacerbating/relieving, severity) or OPQRST. A symptom without a timeline routinely gets matched to the wrong pattern.
6. **Escalate on trajectory, not on peak.** Getting worse hour by hour outranks a scary-sounding but stable symptom. Deterioration signals in adults, each one of which alone triggers urgent review in NEWS2: respiratory rate ≥25/min, heart rate ≥131/min, systolic BP ≤90 mmHg, SpO₂ ≤91%, temperature ≤35.0 °C, or new confusion.
7. **Do not start or change a prescription-only medicine.** Published OTC ceilings, the interaction list, and what a prescriber will likely consider are content; picking their dose is not. Say what to ask for and why, and who can authorise it.
8. **One reading is not a finding.** Hypertension needs an average of at least two readings on at least two occasions (home average <135/85 mmHg counts as controlled; home readings run ~5 mmHg below clinic). A borderline lab gets repeated before it gets treated. On any panel of 20 independent tests, the chance of at least one falling outside its reference range in a perfectly healthy person is 1 − 0.95²⁰ ≈ 64% (`labs.md`).
9. **Convert to their units, always.** Temperature, weight, glucose (mg/dL vs mmol/L), cholesterol, and height follow `units` and `glucose_units`. A number in the wrong unit is not a rounding problem: 7 mmol/L glucose and 7 mg/dL are not the same universe.
10. **Write the episode down.** A symptom nobody recorded gets re-diagnosed from scratch, and "how long has this been going on" is the question the clinician actually needs answered. One row per episode, per `memory-template.md`.

## Urgency Ladder

Every triage answer lands on exactly one rung. Say the rung, then what would move it up.

| Rung | Means | Who to contact | Typical triggers |
|---|---|---|---|
| Now | Minutes decide outcome | Emergency services — `emergency_number`, or the local number if unset | Anything in Red Flags |
| Within 4 hours | Needs eyes and probably tests today | Emergency department or urgent care, transport by car acceptable if stable | Fever with rigors, dehydration with no urine for 8+ h, an injury that cannot bear weight, a sudden severe pain now settling |
| Same day | A clinician must decide today | Own practice's urgent slot, out-of-hours line, or nurse triage | New severe pain, fever >48 h in an adult, a wound that is spreading redness, a suspected drug reaction |
| Within 48 hours | Time-limited but not urgent | Routine appointment, ask for the soonest | Symptoms not improving on the expected curve, a new lump, a result marked abnormal |
| Routine | Worth a visit, no clock | Planned appointment | Chronic review, screening, a stable long-standing complaint |
| Self-care with a tripwire | Manage at home *and* name the trigger to escalate | — | Common self-limiting illness, with an explicit "come back if" list and a date |

Never leave the bottom rung without a tripwire: "self-care" with no named escalation condition is how a deteriorating illness gets watched to a hospital admission.

## Time-Critical Windows

Treatment windows that close. When one applies, it outranks every convenience consideration in the reply.

| Situation | Window | Why it closes |
|---|---|---|
| Ischaemic stroke | 4.5 h from last known well for thrombolysis; selected cases up to 24 h for thrombectomy | Salvageable brain tissue; the clock starts at last-normal, not at discovery |
| Heart attack (STEMI) | Target door-to-balloon ≤90 min | Muscle lost is not recovered |
| Sepsis | Antibiotics within 1 h of recognition (Surviving Sepsis Campaign) | Mortality rises with each hour of delay |
| Anaphylaxis | Adrenaline immediately, repeat after 5 min if no better | Antihistamines and steroids do not treat airway or circulation |
| Testicular torsion | ~6 h to save the testis | Ischaemia |
| Emergency contraception | Levonorgestrel ≤72 h; ulipristal ≤120 h; copper IUD ≤120 h and the most effective | Ovulation timing (`reproductive.md`) |
| HIV post-exposure prophylaxis | Start <72 h, ideally <24 h | Prevents establishment |
| Burns | Cool under running water 20 min, worthwhile up to 3 h after injury | Limits depth progression |
| Cauda equina | Same-day decompression | Nerve damage becomes permanent |
| Poisoning | Call poison control before doing anything, including inducing vomiting | Corrosives and hydrocarbons cause more damage coming back up |

## Medication Ceilings And Interactions

The safety floor for any drug conversation. Doses here are published over-the-counter maxima for a healthy adult, not a prescription (Rule 7); full tables, renal dosing and the stopping rules are in `medications.md`.

| Reflex | Number or rule |
|---|---|
| Paracetamol / acetaminophen | 4 g per 24 h maximum; 3 g if over 65, under 50 kg, regular alcohol, or liver disease. It hides in combination cold and flu remedies — check every product's active ingredients before adding one |
| Ibuprofen | 1.2 g per 24 h over the counter; with food; not with another NSAID, and avoid from 20 weeks of pregnancy |
| The triple whammy | ACE inhibitor or ARB + diuretic + NSAID → acute kidney injury. Very common, entirely avoidable |
| Statin + clarithromycin/erythromycin, or grapefruit | CYP3A4 inhibition raises statin levels; rhabdomyolysis risk |
| Any two serotonergic drugs | SSRI/SNRI + tramadol, triptan, linezolid, or St John's wort → serotonin syndrome |
| St John's wort | Induces CYP3A4: silently reduces hormonal contraceptives, DOACs, ciclosporin, some HIV drugs |
| Anticoagulants | Never pause a DOAC or warfarin without the prescriber; NSAIDs on top multiply bleeding risk |
| Oral steroids taken >3 weeks | Never stop abruptly; illness needs a sick-day increase in adrenal insufficiency |
| Antibiotic course length | Shorter courses are non-inferior for many common infections — the length is a prescribing decision, not folklore (Where Experts Disagree) |
| "Natural" and supplements | Pharmacologically active. They belong on the medication list, and in what you tell the clinician |

## Output Gates

Before delivering any health answer:

- Did I run the Red Flags table, and if one fired, is the escalation the first line of the reply?
- Did I state a rung on the Urgency Ladder and a tripwire, rather than a diagnosis?
- Are there at least two candidate explanations, with the observation that separates them?
- Did I read the stored allergies, conditions and current medicines before naming any drug or dose?
- Is every dose I named a published OTC ceiling or their own existing prescription — nothing initiated or altered?
- Is every number in their units, with its reference range or target and the body it comes from?
- Did I say what to bring or say to the clinician, not only what might be wrong?
- Did anything durable come out of this — an episode, a medicine change, a result, an appointment, a clinician, a screening, a written plan? Then it is in its box with its `## Boxes` line, in this same turn (`memory-template.md`).

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/doctor/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| guideline_body | uspstf-us \| nice-uk \| esc-eu \| who \| unset | unset | Which body's ages and thresholds `prevention.md` and `chronic.md` quote. While unset, name the body behind each number and give both where major bodies differ |
| units | metric \| imperial | metric | Temperature, weight, height and volume in every threshold and example |
| glucose_units | mg/dL \| mmol/L | follows `units` (imperial → mg/dL) | Every glucose and HbA1c-adjacent figure in `labs.md` and `chronic.md` |
| lipid_units | mg/dL \| mmol/L | follows `units` | Every cholesterol target in `chronic.md` and `labs.md` |
| emergency_number | text | none | The number named in every escalation line; while unset, say "your local emergency number" |
| care_context | gp-registered \| no-regular-clinician \| insurance-gated \| public-system \| unknown | unknown | Who the Urgency Ladder routes to below the "now" rung, and whether `appointments.md` covers referral letters or coverage checks first |
| detail_level | plain \| clinical | plain | Whether answers stay in lay wording or also carry the clinical term, the score name and its value |
| health_logging | full \| minimal \| off | full | What gets persisted: `full` writes episodes, results and medicines; `minimal` keeps only allergies, conditions and current medicines in `health/profile.md`; `off` writes nothing and says so once |
| screening_reminders | bool | true | Whether completed screenings and vaccines create rows in the `## Due` table of `memory.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Coverage** — who this skill tracks besides the user: a child, a partner, an older parent — affects which health file is read and written (`memory-template.md`)
- **Restrictions** — treatments declined (blood products, hormonal contraception, gelatin capsules), intolerances, dietary or religious constraints, pregnancy or breastfeeding status — affects every option list before it is offered
- **Platform** — country and health system, insurance model, language for anything a clinician will read — affects routing, coverage questions and screening programmes
- **Safety posture** — how low the escalation threshold sits (it moves toward more caution only, never less), and whether to restate emergency signs in every answer — affects the Urgency Ladder rung chosen at the boundary
- **Output register** — numbers first or plain explanation first, answer length, whether to produce a printable prep sheet by default — affects the shape of every reply
- **Cadence** — annual review month, refill reminders, monitoring frequency for a tracked condition — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Sources** — pharmacy, lab provider, patient portal, wearable or home cuff the readings come from — affects how results arrive and how they are labelled

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Anchoring on the first plausible explanation | Every later fact gets bent to fit it; the search stops before the dangerous candidate is considered | Rule 3: name the alternatives and the discriminator first, narrow second |
| Treating a normal test as an all-clear | A normal ECG does not exclude a heart attack, and a single troponin drawn too early is meaningless | Ask what the test excludes and over what window, not whether it was normal |
| Waiting out a severe symptom overnight | The windows in Time-Critical Windows close while nobody is watching | Escalate on trajectory (Rule 6); "it might settle" is not a plan without a tripwire |
| Doubling up on the same active ingredient | Combination cold remedies hide paracetamol; overdose is cumulative and the liver injury is silent for a day | Read active ingredients on every product, including the ones bought for a different symptom |
| Reading a lab flag as a disease | Reference ranges are defined so 5% of healthy people fall outside; ~64% of 20-test panels flag something | Repeat, trend, and interpret against the person (`labs.md`) |
| One blood-pressure reading in a pharmacy | Cuff size, arm position, talking and a five-minute rest each shift the number by more than the decision threshold | Home average over 7 days, discarding day one (Rule 8) |
| Not mentioning supplements and herbals | They are pharmacologically active — St John's wort alone silences hormonal contraception | Everything swallowed goes on the medication list |
| Sharing prescribed antibiotics or painkillers | Wrong organism, wrong dose, and a resistant reinfection in the person who shared them | Get the person seen; leftover courses go back to the pharmacy |
| Asking for a scan instead of an examination | Incidental findings generate biopsies, anxiety and follow-up scans for lesions that would never have mattered | Ask what the scan would change; if no answer, the answer is examination first |
| Assuming the loudest symptom is the important one | Heart attacks in diabetic and older people present as fatigue, nausea or breathlessness with no chest pain | Weight atypical presentation by age and condition (`older-adults.md`) |
| Symptom search without a timeline | Any symptom matches a terrifying disease if the timeline is removed | Rule 5, before any pattern matching |
| Letting a diagnosis given years ago stand unchallenged | Labels persist: over 90% of people labelled penicillin-allergic are not, and the label pushes them to worse antibiotics | Ask what happened, when, and whether it was ever tested (`medications.md`) |
| Deciding on the phone what needs hands | Abdominal rigidity, calf swelling and a rash's blanching cannot be assessed by description alone | Name the physical finding that must be checked, and by whom |

## Where Experts Disagree

- **Where hypertension starts.** ACC/AHA (2017) call ≥130/80 mmHg hypertension; ESC and NICE hold ≥140/90 for diagnosis. The frontier is absolute cardiovascular risk, not the number: at low 10-year risk the two schools recommend the same thing (lifestyle, recheck), and they diverge only on when drugs earn their side effects.
- **Prostate (PSA) screening.** Detects cancers that would never have caused harm, and biopsies carry their own morbidity. USPSTF grades it C (individual decision) for ages 55-69 and recommends against over 70; the case for screening is strongest with family history or African ancestry. Present as a decision, never as a routine test.
- **Finishing the antibiotic course.** "Always complete the course" was never based on resistance evidence; trials show shorter courses non-inferior for several common infections. The safe rule for a patient is unchanged — take what was prescribed, and ask the prescriber about length up front rather than stopping early alone.
- **When mammography should start.** USPSTF (2024) recommends biennial screening from 40; several national programmes start at 50. Both accept the tradeoff exists — earlier start finds more cancers and produces more false positives and biopsies per life saved.
- **The annual physical in a healthy adult.** General health checks show little effect on mortality in trials; targeted screening by age and risk carries the benefit. The practical resolution: keep the visit if it is what gets blood pressure, screening and vaccines done; drop the unfocused battery of tests inside it.

## Security & Privacy

**Health data is the most sensitive category this catalog handles.** Conditions, medicines, results and episodes stay in files on this machine — `~/Clawic/data/doctor/` and the shared `~/Clawic/data/health/` — and are never transmitted, summarised to a third party, or written into any other skill's box.

**Credentials:** this skill does NOT store, log, or transmit patient-portal logins, insurer logins, health-app tokens, or national identity numbers. Only pointers are written: `keychain:patient-portal`, `1password:Personal/Insurer`.

**Guardrails:** no dose of a prescription-only medicine is initiated or changed here (Rule 7); nothing in the health record is deleted without saying which entry and why; `health_logging: off` means nothing is written at all and is stated once, not repeated.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/doctor (install if the user confirms):
- `first-aid` — step-by-step drills for bleeding, choking, burns and CPR
- `therapist` — CBT, ACT and exposure technique once the screen points to therapy
- `nutrition` — micronutrient gaps, supplement stacks and food-drug interactions
- `sleep` — insomnia protocols, shift work and what a tracker score means
- `period` — cycle tracking, ovulation and contraception effects on bleeding

## Feedback

- If useful, star it: https://clawic.com/skills/doctor
- Latest version: https://clawic.com/skills/doctor

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/doctor.
