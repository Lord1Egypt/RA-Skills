# Mental Health — Screening, Crisis, Medication

Scope here is the medical side: scored screening, risk assessment, physical mimics, what medication does, and when a referral is the answer. Therapy technique — CBT, ACT, exposure, reframing — is `therapist`; ongoing episode logging is `anxiety`.

**Before answering**, read `## Conditions` and `## Medications` in `~/Clawic/data/health/profile.md` (thyroid disease, anaemia, steroids, isotretinoin, beta blockers and alcohol all change the picture) and, if `## Boxes` indexes one, `artifacts/safety-plan.md`.

## Crisis First

Any of these suspends everything else in this file: a stated plan, access to means, an intent with a timeframe, recent self-harm needing medical attention, command hallucinations, or a person unable to keep themselves safe until morning.

The response, in order:

1. **Ask directly.** "Are you thinking about ending your life?" Asking does not plant the idea — that concern has been examined repeatedly and does not hold up.
2. **Ask the three specifics**: a plan, the means, and a timeframe. Plan plus available means is a different level of risk from a wish that things would stop.
3. **Do not leave them alone.** Stay on the line or with them until someone else has them.
4. **Route now**: the local crisis line or emergency number (`emergency_number`), or the emergency department. Where `emergency_number` is unset, say "your local emergency or crisis line" rather than guessing a number.
5. **Reduce access to means** in the same conversation — medicines, firearms, keys. This is the single intervention with the best evidence behind it, because most acute crises pass within hours.
6. **Follow up with a time**, not a hope: who is checking in, and when.

Never negotiate secrecy about acute risk, and never respond with a distraction technique.

## Scored Screens

Scores make a vague conversation actionable and give the clinician something to act on. Each is a screen, not a diagnosis.

| Instrument | Measures | Reading it |
|---|---|---|
| PHQ-9 | Depression, 9 items, past 2 weeks | 5-9 mild · 10-14 moderate · 15-19 moderately severe · 20+ severe. **≥10 is the usual referral threshold.** Item 9 asks about self-harm — any positive answer triggers the crisis protocol above regardless of total |
| GAD-7 | Anxiety, 7 items | 5-9 mild · 10-14 moderate · 15+ severe; ≥10 warrants assessment |
| AUDIT-C | Alcohol, 3 items | ≥4 in men, ≥3 in women is a positive screen; positive is common and is a conversation, not a verdict |
| PHQ-2 / GAD-2 | Two-item versions | Fast pre-screen; positive → run the full instrument |
| Mood chart | Bipolar pattern | Ask about sustained periods of reduced sleep need with elevated energy — antidepressants alone can destabilise undiagnosed bipolar disorder |

## What Is Not Psychiatric Until Excluded

New psychological symptoms deserve a physical scan of causes, especially at a first presentation or an unusual age.

- **Thyroid disease** — anxiety, weight and heart-rate change (hyper); low mood, fatigue, cold (hypo).
- **Anaemia and B12 deficiency** — fatigue, low mood, cognitive fog.
- **Sleep apnoea** — snoring, witnessed pauses, morning headache, unrefreshing sleep; presents as depression and treatment-resistant fatigue.
- **Medicines** — steroids, isotretinoin, hormonal contraception in a susceptible minority, beta blockers, varenicline, stimulant withdrawal.
- **Alcohol and cannabis** — both cause the anxiety they are used to treat; withdrawal from alcohol produces tremor, sweating and, dangerously, confusion and seizures.
- **Delirium** in an older adult is a medical emergency and is not depression (`older-adults.md`).
- **Perimenopause and postpartum** — mood change with a hormonal timeline of its own (`reproductive.md`).

## Panic Versus Cardiac

Panic attacks peak within about 10 minutes and settle within 20-30, with tingling around the mouth and in the fingers, a sense of unreality, and a fear of dying. That said: a **first** episode, an episode over 45, exertional onset, or one with syncope gets a cardiac work-up before it is labelled panic. The label is safe only after the alternative was considered once.

## What Medication Does And Does Not Do

- Antidepressants take time: a first change in 1-2 weeks, meaningful improvement typically 4-6 weeks, full effect 8-12. Judging effect before 4 weeks at an adequate dose is the most common reason a working drug gets abandoned.
- The first two weeks often feel worse — nausea, jitteriness, disturbed sleep. Knowing this in advance is what gets people through it.
- Under-25s carry a documented increase in suicidal thoughts in the early weeks: closer monitoring in that window is standard, not a reason to withhold treatment.
- Stopping is tapered over weeks; abrupt discontinuation causes dizziness, electric-shock sensations and mood swings, which are withdrawal, not relapse (`medications.md`).
- Benzodiazepines work fast and stop working: tolerance and dependence develop within weeks, and combined with opioids or alcohol they suppress breathing.
- Medication and therapy together beat either alone in moderate-to-severe depression. For mild presentations, therapy and exercise carry most of the effect.

## Self-Harm And Eating Disorders

- Self-harm without suicidal intent still needs the risk conversation and wound care, and it raises future suicide risk — it is never dismissed as attention-seeking.
- Eating-disorder red flags that are medical rather than psychological: rapid weight loss, fainting, resting heart rate under 50, low blood pressure, cold intolerance, electrolyte disturbance, vomiting after meals, or amenorrhoea. Those are same-day, because the complications are cardiac. Weight-focused advice is withheld until an eating disorder has been excluded — this rule overrides anything in `calories` or `dietitian`.

## Where This Goes

**Write in the same turn** (`memory-template.md`), and only what `health_logging` allows:

- Screen scores with their date → `## Measurements` in `~/Clawic/data/health/profile.md` as `PHQ-9 14 (2026-07-26)`; once a single instrument passes ~15 entries it moves to `~/Clawic/data/health/phq9.md` with the same headings, the copy is deleted, and one index line stays behind.
- A crisis or a safety plan → `~/Clawic/data/doctor/artifacts/safety-plan.md`: warning signs, coping steps that have worked, people to contact by name (from `~/Clawic/data/contacts/contacts.md`), the crisis line, and how means were reduced. Its `## Boxes` line reads "read at the first sign of crisis" and is written the same turn.
- Medication starts, stops and side effects → `## Medications` in the shared profile, in place.
- Review dates — the 2-week check after starting an antidepressant, the next screen — → `## Due`.
- This is the most sensitive material this skill stores. It stays local, it is never summarised into another skill's box, and `health_logging: off` means none of it is written at all.
