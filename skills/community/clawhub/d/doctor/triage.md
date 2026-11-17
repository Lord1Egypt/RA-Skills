# Triage — How Urgent Is This

The one question behind almost every health message. The output is a rung on the Urgency Ladder (SKILL.md), a tripwire, and the sentence to say when they make contact.

**Before triaging**, read `~/Clawic/data/health/profile.md` — conditions, current medicines, allergies, pregnancy status — and `## Current Concerns` in `~/Clawic/data/doctor/memory.md`. The same symptom means different things in someone on anticoagulants, immunosuppressed, pregnant, over 75, or two weeks post-operative. If `## Boxes` points to an episode log, check whether this symptom has happened before and what it turned out to be.

## The Four Questions, In Order

1. **Is anything in the Red Flags table present?** If yes, stop and escalate — no differential, no reassurance, no alternatives.
2. **What is the trajectory?** Better, stable, or worse over the last 6-12 hours. Worsening beats severity: a moderate pain doubling every two hours outranks a severe pain that has been identical for a week.
3. **Who is this happening to?** Age under 3 months or over 75, pregnancy, immunosuppression (chemotherapy, transplant, high-dose steroids, poorly controlled diabetes), anticoagulation, recent surgery or hospital stay, no spleen. Each shifts the answer up one rung on its own.
4. **What is the worst thing this could be, and how would I know it is not that?** Name the exclusion test — an observation, not a hope.

## Red Flags By System

Everything in the SKILL.md table, plus the ones that only show up when you go system by system.

| System | Escalate now on |
|---|---|
| Cardiac | Chest pain >15 min or with sweating/nausea; syncope during exertion or while lying flat; palpitations with chest pain or fainting; new breathlessness lying flat with leg swelling |
| Neuro | Any FAST sign; thunderclap headache; new focal weakness or numbness; first seizure or a seizure >5 min; head injury with vomiting, worsening headache, or anticoagulation |
| Respiratory | Cannot speak a full sentence; SpO₂ ≤91% (≤88% if known COPD with a documented 88-92% target); stridor; coughing frank blood |
| Abdominal | Rigid abdomen; pain with a pulsatile mass or radiating to the back in anyone over 60; vomiting with no flatus or stool; testicular pain <6 h; pain in pregnancy |
| Infection | Rash that does not blanch; rigors with confusion; fever with a prosthetic joint or valve, or in someone neutropenic; spreading redness with a line marching up a limb |
| Urinary | No urine for 8+ h with abdominal pain (retention); flank pain with fever; visible blood in urine with clots |
| Vascular | One-sided calf swelling with pain; a cold, pale, pulseless limb; sudden severe back or abdominal pain in a smoker over 60 |
| Eye | Sudden painless visual loss; a curtain across vision; painful red eye with a fixed pupil or halos; chemical splash |
| Mental health | Stated plan, means and intent; command hallucinations; withdrawal from alcohol with tremor and confusion |
| Obstetric | Any bleeding in pregnancy; reduced fetal movements; headache with visual change past 20 weeks |

## Ambulance Or Car

- **Ambulance** when treatment starts in the vehicle or the person could deteriorate en route: suspected stroke or heart attack, breathing difficulty, altered consciousness, anaphylaxis, major bleeding, seizure, suspected spinal injury. Being driven by a relative delays a stroke pathway that begins with a pre-alert call to the hospital.
- **Car** when the person is stable, breathing normally, alert, and the trip is under about 20 minutes with someone else driving.
- **Never drive yourself** with chest pain, altered consciousness, one-sided weakness, or after taking sedating medicine.
- If the choice is unclear, the emergency line itself triages — calling is not an escalation, it is the assessment.

## What To Say When They Make Contact

The order matters because the person answering is triaging on the first fifteen seconds.

1. Age, sex, and the one-line problem: "62-year-old man, chest pain for 40 minutes."
2. When it started and whether it is getting worse.
3. The high-risk context: pregnancy, anticoagulants, immunosuppression, recent surgery, known conditions.
4. Vital signs if measured, with units and the time taken.
5. What has already been taken or done.

For a non-urgent booking, the phrase that gets an appropriate slot is the symptom plus the duration plus the change: "cough for three weeks, now with blood-streaked sputum" beats "I have a cough".

## Tripwires — Every Self-Care Answer Needs One

A self-care answer is incomplete without an explicit, observable escalation trigger and a date. Template:

> Manage at home. Contact [rung] **if** any of: [symptom crosses a named threshold] · [a new symptom appears] · [no improvement by <date>].

Threshold examples that work because they are observable: temperature above 39 °C for more than 48 h · fewer than 4 wet nappies in 24 h · unable to walk on it after 48 h · breathing rate you can count rising above 25/min · redness spreading past a line drawn on the skin with a pen. Vague tripwires ("if it gets worse") are not tripwires; the person is already worried, and "worse" is exactly what they cannot judge.

## Reassurance That Is Actually Safe

Reassurance is legitimate when it comes with three parts: what makes the benign explanation likely, what has been excluded and how, and the tripwire. Reassurance without the third part is the most common way a triage answer causes harm — the person stops watching.

## Where This Goes

**After any triage, write it down in the same turn** (`memory-template.md`): a row in `~/Clawic/data/doctor/episodes/<year>.md` with the date, the symptom, the rung given, the tripwire, and — once known — how it resolved. Update `## Current Concerns` in `memory.md` while it is live and clear the line when it closes. A symptom that recurs is a different problem from one that happens once, and only the log can tell them apart. If the episode produced an escalation plan the user will reuse (a known migraine pattern, a recurring flare), that plan is an artifact: `~/Clawic/data/doctor/artifacts/<kebab-name>.md`, with its `## Boxes` line the same turn.
