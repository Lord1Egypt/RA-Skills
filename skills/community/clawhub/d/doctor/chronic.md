# Chronic Conditions — Targets, Monitoring, Flares

A long-term condition is managed by three things the person can hold: a target, a monitoring interval, and a written plan for when it gets worse. Everything else is detail.

**Before answering**, read `## Conditions` and `## Measurements` in `~/Clawic/data/health/profile.md`, any `~/Clawic/data/health/<metric>.md` the `## Boxes` index names, and the `## Due` table in `~/Clawic/data/doctor/memory.md` — state any overdue review in one line, as a statement, not a question. Targets are individualised by the treating clinician; where `guideline_body` is unset, name the body behind each number and flag where major bodies differ.

## Targets Worth Knowing

| Condition | Common target | The nuance that changes it |
|---|---|---|
| Hypertension | Clinic <140/90 mmHg (NICE, ESC); ACC/AHA treat from 130/80. Home average <135/85 counts as controlled | Home readings run about 5 mmHg below clinic. Over 80, a higher systolic target is usually accepted; falls and dizziness outrank the number |
| Type 2 diabetes | HbA1c <7.0% (53 mmol/mol) for most adults | Relaxed to 7.5-8.0% in frailty, limited life expectancy, or hypoglycaemia risk; tighter early after diagnosis in young people |
| Lipids | LDL <2.6 mmol/L (100 mg/dL) general; <1.8 (70) with established cardiovascular disease; <1.4 (55) very high risk per ESC | The decision is driven by 10-year total risk, not by the lipid value alone |
| Asthma | No night waking, reliever ≤2 days/week, no activity limitation | **Reliever use ≥3 times a week means the condition is not controlled**, whatever the person says about it. More than one reliever inhaler a month is a red flag |
| COPD | Function, not numbers: exacerbations per year, walking distance | Oxygen target 88-92% rather than 94%+ — a normal-looking saturation can be dangerous here |
| Hypothyroidism | TSH inside the lab range, symptoms resolved | Levothyroxine absorption is destroyed by calcium, iron and coffee — separate by 4 hours, same time each day |
| Chronic kidney disease | Slow the decline: blood pressure, glucose, avoid NSAIDs | eGFR <60 for ≥3 months defines it; every new drug gets a renal-dose check (`medications.md`) |
| Migraine | Fewer than 4 headache days a month, and abortive treatment that works | Painkillers on ≥10-15 days a month cause medication-overuse headache — the treatment becomes the disease |
| Reflux | Symptom control on the lowest effective step | Alarm symptoms — difficulty swallowing, weight loss, vomiting blood, anaemia, new onset over 55 — are investigated, not treated blind |
| Atrial fibrillation | Stroke prevention first, rate or rhythm second | Anticoagulation is decided by risk score, not by how the person feels |

## Monitoring Cadence

Every row here becomes a `## Due` line with its last-run date; a cadence with no recorded last run gets skipped for two quarters and nobody notices.

| Condition | Typical interval | What is checked |
|---|---|---|
| Hypertension | 6-12 months when stable; 4-6 weeks after a dose change | Home BP series, kidney function and potassium if on ACE/ARB or diuretic |
| Type 2 diabetes | HbA1c every 3-6 months; annual review | Feet, eyes (retinal screening), kidneys (urine albumin), lipids, blood pressure |
| Asthma | Annual review; after every exacerbation | Inhaler technique, reliever count, action plan, adherence to preventer |
| Thyroid on replacement | 6-8 weeks after any dose change, then annually | TSH |
| Statin | 3 months after starting, then annually | Lipids, liver enzymes once |
| CKD | 6-12 months by stage | eGFR, urine albumin:creatinine, potassium |
| Any condition on ≥5 medicines | Annual, or 6-monthly over 75 | Full medication review (`older-adults.md`) |

## Home Measurement, Done So The Number Means Something

- **Blood pressure**: sit 5 minutes, back supported, feet flat, arm supported at heart level, no talking, no caffeine or exercise for 30 minutes. Take two readings a minute apart and keep the second in `## Measurements` of the shared profile, morning and evening, for 7 days; **discard day one** and average the rest. A cuff too small for the arm can add 10-30 mmHg — the single largest source of a wrong diagnosis at home.
- **Glucose**: what matters is the pattern by time of day, not isolated numbers. Wash hands first; fruit residue produces spectacular false highs.
- **Peak flow**: best of three efforts, same time of day, compared against the person's own best rather than a predicted value.
- **Weight**: same scale, same time, same clothing, weekly rather than daily for trend.

## Flare And Action Plans

A written action plan turns "I feel worse" into a decision. The shape is the same for asthma, COPD, heart failure and inflammatory conditions:

- **Green** — usual state, usual treatment, with the observable that defines it (peak flow above X, weight stable, reliever ≤2 days/week).
- **Amber** — early deterioration, the specific step-up agreed with the clinician, and the date to review it.
- **Red** — the observable that means urgent help now, and who to call.

Plans built around a measured number beat plans built around how the person feels, because feeling adapts to a slow decline. Written plans reduce hospital admissions in asthma and COPD, which is why the plan itself is worth the visit.

## Sick-Day Rules

Any illness with vomiting, diarrhoea or fever with poor intake temporarily changes the regimen: several drugs pause (SADMANS — sulfonylureas, ACE inhibitors, diuretics, metformin, ARBs, NSAIDs, SGLT2 inhibitors) and replacement steroids increase (`medications.md`). Diabetes adds its own: never stop insulin during illness even when not eating, check glucose more often, check ketones if type 1 and glucose is high, and keep drinking.

## Living With It

- **Adherence** is not a character trait: the reasons are cost, side effects, complexity, and not believing the drug does anything. Ask which one, then solve that one. Simplifying to once daily and aligning doses to an existing habit beats reminders.
- **Exercise** is treatment in hypertension, type 2 diabetes, depression, osteoarthritis and heart failure, with effect sizes comparable to some drugs — but it is prescribed with a starting dose and progression like anything else (`fitness`).
- **Sleep and mood** deteriorate under any chronic condition and worsen it in return; screening for depression is part of chronic care, not a separate topic (`mental-health.md`).
- **Multimorbidity** is the normal case, and guidelines written for one condition collide: the goal becomes what the person values, not every target at once (`older-adults.md`).

## Where This Goes

**Write in the same turn** (`memory-template.md`):

- The condition, its date of diagnosis and its agreed target → `## Conditions` in `~/Clawic/data/health/profile.md`, updated in place.
- Every measured value with its unit → `## Measurements` in the same file, moving to `~/Clawic/data/health/<metric>.md` once a single metric passes ~15 entries (delete the copy, keep one index line).
- Every monitoring interval agreed → a row in `## Due` of `~/Clawic/data/doctor/memory.md` with the last-run date.
- The written action plan → `~/Clawic/data/doctor/artifacts/action-plan-<condition>.md`, born as its own file the first time it exists, with its `## Boxes` line and the read condition "read at the first sign of a flare".
- A treatment decision with a reason — why this drug and not that one, why the target was relaxed — goes in the same artifact under `## Decisions`, so it is not re-litigated at the next appointment by someone with no memory of it.
