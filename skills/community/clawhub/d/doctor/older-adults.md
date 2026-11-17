# Older Adults — Polypharmacy, Falls, Delirium

Three things break the standard playbook after about 75: presentations become atypical, medicines that were right at 60 become harmful, and the goal shifts from treating every condition to protecting function.

**Before answering**, read the person's health file — `~/Clawic/data/health/profile.md` for the user, or `~/Clawic/data/health/<name>.md` for a parent or relative if `## Boxes` indexes one — with attention to the full medicine list, kidney function, and what their baseline actually is. **Baseline is the single most valuable stored fact here**: "confused" means nothing without knowing whether they normally do the crossword.

## Atypical Presentation

Serious illness in older adults often arrives without its textbook signs. The four presentations that cover most of it:

| Presentation | Frequently caused by |
|---|---|
| New confusion or drowsiness | Infection, dehydration, medicines, retention, constipation, pain, hypoxia, stroke |
| A fall or "off legs" | Infection, arrhythmia, anaemia, postural hypotension, medicines, a fracture already sustained |
| Not eating, withdrawn | Infection, depression, constipation, pain, dental problems |
| A new incontinence | Retention with overflow, infection, delirium, medicines |

Fever is often absent — a temperature of 37.5 °C in a frail 85-year-old may represent significant infection, and hypothermia below 36 °C is a sepsis sign in this group. Heart attacks present as breathlessness, fatigue or a fall rather than chest pain.

## Delirium Versus Dementia

| | Delirium | Dementia |
|---|---|---|
| Onset | Hours to days | Months to years |
| Course | Fluctuates through the day, often worse at night | Slowly progressive |
| Attention | Impaired — cannot follow a sentence or list months backwards | Relatively preserved early |
| Consciousness | Clouded or hyperalert | Clear until late |
| Reversible | Usually, if the cause is found | No |

**Delirium is a medical emergency**, not a psychiatric one, and it carries a substantial mortality. Screening tools like the 4AT are quick and score alertness, orientation, attention (months backwards) and acute change; a score of 4 or more suggests delirium. Look for the cause: infection, urinary retention, constipation, dehydration, pain, a new medicine, alcohol withdrawal, hypoxia.

Antipsychotics are not the first response — reorientation, hydration, glasses and hearing aids, daylight, sleep, and removing the offending drug are.

## Polypharmacy

- Five or more regular medicines is the usual definition; risk of an adverse interaction climbs steeply with each addition, and above about ten medicines it is close to a certainty that one is causing a symptom.
- **The prescribing cascade** is the pattern to hunt: a drug causes a symptom, the symptom gets its own drug. Amlodipine → ankle swelling → a diuretic. A cholinesterase inhibitor → urinary urgency → an anticholinergic that worsens cognition. Ask of every new symptom: which drug started before it?
- **Anticholinergic burden** accumulates invisibly across sedating antihistamines, bladder antimuscarinics, tricyclics, some antipsychotics and antiemetics; the total predicts falls, confusion and retention better than any single drug does.
- Structured tools exist — Beers criteria, STOPP/START — and their common core is: benzodiazepines and Z-drugs, anticholinergics, long-term NSAIDs, and sulfonylureas with hypoglycaemia risk.
- **Deprescribing** is planned, one drug at a time, with a monitoring interval and a written reason. An annual medication review (6-monthly over 75 or above 10 medicines) is a `## Due` row, not an intention.
- Renal function falls with age even when creatinine reads normal, because muscle mass falls too. Every new prescription gets a renal check (`medications.md`).

## Falls

- **Any fall plus a gait or balance problem, or two or more falls in a year, warrants a multifactorial assessment.** A fall is a symptom, and the assessment is the treatment.
- What the assessment covers: postural blood pressure (a drop of ≥20 systolic or ≥10 diastolic on standing), vision, footwear, medicines that sedate or drop pressure, alcohol, cognition, continence, home hazards, and strength and balance.
- What actually reduces falls: strength and balance training as an ongoing programme, medication review, treating vision, and vitamin D where deficient. Hip protectors and alarms manage consequences, not risk.
- **After any fall in someone on anticoagulants, a head strike is assessed the same day** even with no symptoms — the bleed can be slow (`injuries.md`).
- Fear of falling produces its own decline through inactivity; the intervention is graded activity, not more rest.

## Frailty And What The Goal Is

Frailty is a state where a small insult produces a disproportionate decline. Recognisable markers: slow walking speed, unintentional weight loss, exhaustion, weakness, low activity.

In frailty, standard disease targets are relaxed deliberately, and this is good care rather than giving up: HbA1c targets loosen to 7.5-8.0% because hypoglycaemia causes falls; blood pressure targets loosen because postural drops cause falls; statins started for primary prevention in the very old have little time to pay off. The question that reorders everything: **what matters most to this person — years, or the ability to keep doing something specific?**

## The Things Nobody Asks About

- **Hearing and vision** — untreated hearing loss accelerates cognitive decline and social withdrawal, and hearing aids are among the highest-value interventions available in this group.
- **Continence** — treatable and rarely raised without prompting.
- **Constipation** — a common cause of confusion, retention and abdominal pain, and made worse by half the medicine list.
- **Oral health and dentures** — a direct driver of poor nutrition.
- **Loneliness** — carries mortality risk comparable to well-recognised medical risk factors, and it is a legitimate item on a problem list.
- **Driving** — a real safety question, and one that a clinician can assess formally rather than a family arguing about it.

## Advance Care Planning

Best done long before the crisis, in calm conditions. Four components: who decides if the person cannot (health proxy or power of attorney), what treatments they would decline, where they would prefer to be cared for, and what "a good outcome" means to them. A resuscitation decision is a clinical decision informed by that conversation, and it is specific to CPR — it never means withholding other treatment, a misunderstanding that causes real harm.

## Caregivers

The caregiver's own state is part of the clinical picture: exhaustion, isolation, their own missed appointments and their own medicines. Ask directly. Respite, carer assessments and support services exist and are systematically under-claimed.

## Where This Goes

**Write in the same turn** (`memory-template.md`): a relative whose health this skill also tracks gets their own file in the shared health box — `~/Clawic/data/health/<kebab-name>.md`, opening with `# Health — <Name>` and the same headings as `profile.md` — with its `## Boxes` line and the read condition "read before any question about <Name>", and their person row in `~/Clawic/data/contacts/contacts.md` with `Role: parent` or similar. **Record the baseline explicitly** in `## Conditions` — normal cognition, normal mobility, who they live with — because every future "is this new?" question is answered against it. Falls go to `~/Clawic/data/doctor/episodes/<year>.md` with the circumstances. The medication review date is a `## Due` row. A deprescribing plan or an advance care plan summary is an artifact: `~/Clawic/data/doctor/artifacts/<kebab-name>.md`, with its `## Boxes` line the same turn. Legal documents themselves are not copied here — the artifact records that they exist, where, and who holds them.
