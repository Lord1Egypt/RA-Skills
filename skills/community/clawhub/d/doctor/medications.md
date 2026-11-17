# Medications — Safety, Interactions, Stopping

This skill never initiates or changes a prescription-only dose (SKILL.md Rule 7). What it does: check the combination, catch the ceiling, explain the side effect, and produce the exact question for the prescriber or pharmacist.

**Contents:** [Read The List First](#read-the-list-first) · [OTC Ceilings](#otc-ceilings) · [Interaction Classes That Actually Cause Harm](#interaction-classes-that-actually-cause-harm) · [Kidneys, Liver, Age And Pregnancy](#kidneys-liver-age-and-pregnancy) · [Side Effect Or Coincidence](#side-effect-or-coincidence) · [Missed Doses](#missed-doses) · [Stopping](#stopping) · [Allergy Versus Intolerance](#allergy-versus-intolerance) · [Sick-Day Rules](#sick-day-rules) · [Storage, Expiry, Supply](#storage-expiry-supply) · [Where This Goes](#where-this-goes)

## Read The List First

**Before naming any drug**, read `## Medications`, `## Allergies` and `## Conditions` in `~/Clawic/data/health/profile.md`. The list must include what people do not think of as medicines: supplements, herbals, eye drops, inhalers, patches, contraception, anything bought over the counter, and anything borrowed. Roughly half of clinically important interactions involve one item from that second group.

The question that surfaces the missing ones: "anything you take that you would not call a medicine — vitamins, herbal, drops, patches, something for sleep?"

## OTC Ceilings

Published maxima for a healthy adult. These are the numbers on the packet, not a prescription.

| Drug | Adult ceiling | The trap |
|---|---|---|
| Paracetamol / acetaminophen | 4 g per 24 h; **3 g** if over 65, under 50 kg, regular alcohol, malnourished, or liver disease | It is inside combination cold, flu and night-time remedies under other names. Overdose is cumulative, painless for a day, and a leading cause of acute liver failure |
| Ibuprofen | 1.2 g per 24 h over the counter (higher only on prescription) | Not with another NSAID including aspirin doses used for pain; avoid from 20 weeks of pregnancy, in known kidney disease, and in heart failure |
| Naproxen OTC | 660 mg per 24 h where sold without prescription | Same NSAID cautions; longer acting, so accidental double-dosing lasts longer |
| Aspirin for pain | 4 g per 24 h in adults | Never for pain in under-16s (Reye's syndrome). Low-dose aspirin for the heart is a different drug decision entirely |
| Antihistamines (sedating) | Per packet | Impairs driving into the next morning; a common cause of falls and confusion in older adults |
| Decongestants (pseudoephedrine, oxymetazoline) | 3-5 days maximum for nasal sprays | Rebound congestion; raises blood pressure and interacts with several antidepressants |
| Codeine-containing OTC products | 3 days maximum | Dependence and rebound headache; ineffective in the ~7% of people who cannot metabolise it |
| Proton pump inhibitors OTC | 14 days per course | Symptom masking; taking it "until it settles" hides the alarm symptoms that need investigating |

## Interaction Classes That Actually Cause Harm

Learning the classes beats memorising pairs, because the classes generalise to new drugs.

| Class | Mechanism | Example combination | What happens |
|---|---|---|---|
| Triple whammy | Reduced renal perfusion from three directions | ACE inhibitor or ARB + diuretic + NSAID | Acute kidney injury, especially during a dehydrating illness |
| Bleeding stack | Additive haemostatic impairment | Warfarin or DOAC + NSAID, SSRI, or aspirin | Gastrointestinal bleed; SSRIs are the one people never suspect |
| CYP3A4 inhibition | Drug levels rise | Statin + clarithromycin, azole antifungals, or grapefruit | Muscle damage, rhabdomyolysis |
| CYP3A4 induction | Drug levels fall silently | St John's wort or rifampicin + hormonal contraception, DOAC, ciclosporin, some HIV drugs | Contraceptive failure, transplant rejection, clot |
| Serotonin excess | Additive serotonergic load | SSRI/SNRI + tramadol, triptan, linezolid, or MAOI | Agitation, tremor, hyperthermia — hours after starting |
| QT prolongation | Additive cardiac repolarisation delay | Citalopram + ondansetron + a macrolide | Arrhythmia; risk multiplies with low potassium |
| Sedative load | Additive CNS depression | Opioid + benzodiazepine + alcohol or gabapentinoid | Respiratory depression; the commonest fatal accidental combination |
| Potassium stack | Additive retention | ACE inhibitor/ARB + spironolactone + potassium supplement or salt substitute | Hyperkalaemia, arrhythmia |
| Absorption blocks | Chelation or pH change | Levothyroxine or antibiotics + calcium, iron, or antacids | The drug simply does not work; separate doses by 4 hours |
| Anticholinergic burden | Additive across many drugs | Sedating antihistamine + bladder drug + tricyclic | Confusion, falls, retention, especially over 65 (`older-adults.md`) |

Practical rule: any new medicine gets checked against the full list including supplements, and any new symptom appearing within days to weeks of a new medicine is assumed drug-related until reasoned out.

## Kidneys, Liver, Age And Pregnancy

- **Kidneys** decide the dose for a long list of common drugs. eGFR below 60 sustained for three months is chronic kidney disease; metformin is cautioned below 45 and stopped below 30; several antibiotics, gabapentinoids, DOACs and opioids need reduction. Renal function falls with age even when creatinine looks normal, because muscle mass falls with it.
- **Liver** disease changes paracetamol ceilings and the handling of many sedatives and statins.
- **Pregnancy and breastfeeding** are a hard gate before any recommendation. The NSAID threshold, canonical for this skill: **avoid from 20 weeks of pregnancy** — every NSAID, not only ibuprofen (FDA 2020, on the risk of low amniotic fluid; the older "third trimester" rule covered only premature ductal closure, so 20 weeks is the one to apply). Most tetracyclines, retinoids, several antiepileptics and warfarin carry their own specific risk. Note the status in `config.yaml` under the restrictions preference area the moment it is stated, and check it every time.
- **Weight matters in children** — every paediatric dose is per kilogram (`children.md`).

## Side Effect Or Coincidence

Four questions, in order: did it start after the drug did · does the timing match the known onset window for that class · has it happened before with the same or a related drug · does anything else explain it. Withdrawal and re-challenge are a prescriber's decision, never a self-experiment for anything cardiac, psychiatric, or anticoagulant.

Common ones worth naming because the person will not connect them: ACE inhibitor → dry cough, sometimes months later · statin → muscle ache (real, but far less common than attributed; the nocebo effect is large) · metformin → diarrhoea that usually settles or resolves on the modified-release form · beta blocker → fatigue and cold hands · amlodipine → ankle swelling · SSRIs → nausea and jitteriness for the first two weeks, sexual side effects that persist · gabapentinoids and sedating antihistamines → falls · PPIs → low magnesium on long-term use · steroids → mood change, glucose rise, sleep loss.

## Missed Doses

The general rule: take it when remembered, unless it is nearly time for the next one — then skip it. Never double up. Four exceptions where the specifics matter:

- **Combined hormonal contraception**: one missed pill is taken as soon as remembered; two or more in the first week needs emergency contraception if there was unprotected sex, plus seven days of condoms (`reproductive.md`).
- **Anticoagulants**: follow the drug's own written instruction; the bleeding-versus-clot balance is not a general rule.
- **Insulin**: depends entirely on the type and the meal; contact the diabetes team rather than guessing.
- **Antiepileptics and Parkinson's medication**: timing is the treatment; a missed dose is followed up with the prescriber rather than absorbed silently.

## Stopping

- **Never stop abruptly**: oral steroids taken more than about three weeks (adrenal crisis), beta blockers (rebound tachycardia and ischaemia), clonidine (rebound hypertension), benzodiazepines (seizure risk), antiepileptics, antidepressants (discontinuation symptoms — taper over weeks), opioids in a dependent user.
- **Safe to stop when the reason is gone**: a course-limited antibiotic finished as prescribed, a short PPI course, a symptomatic painkiller.
- Deprescribing is a legitimate goal, not a failure of care — the review conversation belongs with the prescriber and is scheduled, not improvised (`older-adults.md`).

## Allergy Versus Intolerance

| Label | What it looks like | Consequence of getting it wrong |
|---|---|---|
| True allergy | Urticaria, angioedema, wheeze, anaphylaxis, or a severe delayed skin reaction with blistering | Re-exposure can kill |
| Intolerance | Nausea, diarrhoea, headache, a metallic taste | Recorded as "allergy", it removes the best drug from the list forever |

Over 90% of people labelled penicillin-allergic are not allergic on testing, and the label pushes them towards broader antibiotics with worse outcomes and more resistance. Ask what happened, how soon after the dose, and how old they were. **Record the reaction, not just the word**: `## Allergies` in `~/Clawic/data/health/profile.md` takes drug, reaction, and year. An allergy line with no reaction described is the one clinicians cannot act on.

## Sick-Day Rules

During any illness with vomiting, diarrhoea, or fever with poor intake, several regular medicines are temporarily paused because dehydration turns them harmful. The commonly listed group (SADMANS): sulfonylureas, ACE inhibitors, diuretics, metformin, ARBs, NSAIDs, and SGLT2 inhibitors. This is a plan agreed in advance with the prescriber, written down, and followed — not improvised mid-illness.

The opposites, which must be *increased* rather than paused: replacement steroids in adrenal insufficiency, typically doubled during febrile illness per the person's written emergency plan.

## Storage, Expiry, Supply

- Heat and bathroom humidity degrade tablets faster than the date suggests; insulin, some antibiotics and adrenaline autoinjectors have specific storage rules and adrenaline should never be left in a hot car.
- Expiry on rescue medicine (autoinjector, GTN spray, inhaler, glucagon) is not a paperwork detail — it is a row in `## Due` with the expiry date, because the day it is needed is the day nobody checks.
- Never share prescribed medicines, and return unused ones to a pharmacy rather than keeping them for next time.
- Travelling: carry medicines in original labelled packaging with a copy of the prescription list; check controlled-drug rules for the destination well ahead (`prevention.md`).

## Where This Goes

**Write in the same turn** (`memory-template.md`): every start, stop, dose change or brand switch updates the medicine's row in `## Medications` of `~/Clawic/data/health/profile.md` — name, dose, frequency, why, prescriber, start date — updated **in place**, never appended as a second row for the same drug; a stopped medicine keeps its row with `stopped <date> — <reason>` until the next review, because "why did we stop that" is the question that comes back. Reactions and allergies go to `## Allergies` with the reaction described and the year. Repeat-prescription and rescue-medicine expiry dates become rows in `## Due`. A written sick-day or steroid emergency plan is an artifact: `~/Clawic/data/doctor/artifacts/sick-day-plan.md`, with its `## Boxes` line the same turn and the read condition "any illness with vomiting, diarrhoea or fever".
