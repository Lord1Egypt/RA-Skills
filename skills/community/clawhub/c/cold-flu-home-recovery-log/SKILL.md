---
name: cold-flu-home-recovery-log
description: Create a short-term home recovery log for a cold, flu, or similar illness, including symptom timeline, temperature entries, hydration and rest notes, user-entered medication timing, red-flag checklist, and a clinician-ready summary. Use when someone wants practical illness tracking without diagnosis, medication advice, or replacement of medical care.
---

# Cold & Flu Home Recovery Log

## Overview

Use this skill when a user wants a simple, short-term record for a cold, flu, or similar home illness. Focus on organizing observations, tracking changes over time, supporting caregiver handoffs, and preparing a concise summary if the user contacts a clinician, school, workplace, or family member.

This is a prompt-only health organization skill. It does not diagnose, prescribe, recommend medication changes, interpret symptoms as a condition, or replace professional medical care.

## Trigger

Use this skill when the user says they need to:

- Track cold or flu symptoms at home.
- Build a symptom log for themselves, a child, or another household member.
- Remember temperature, hydration, rest, appetite, and energy changes.
- Record when over-the-counter medicine or home care steps were taken as user-entered facts.
- Prepare a short update for a clinic, school, workplace, or caregiver.
- Decide what information to have ready before calling a medical professional.

Do not use this skill to diagnose the illness, choose medications, calculate doses, recommend treatment, or decide whether symptoms are safe to ignore.

## Intake

Ask only for practical tracking details the user is comfortable sharing:

- Illness start date or estimated first symptom date.
- Age group, such as infant, child, teen, adult, older adult, or high-risk person if relevant.
- Main symptoms and whether they are improving, stable, or worsening.
- Temperature readings, if available, with date and time.
- Sleep, rest, hydration, appetite, and energy notes.
- User-entered medications or home-care steps already taken, including timing and dose only if the user provides it.
- School, work, caregiving, or household communication needs.
- Any specific concerns that make the user think professional guidance may be needed.

Do not ask for unnecessary private medical history. If the user volunteers sensitive medical details, use them only to organize the log and encourage appropriate professional care when needed.

## Workflow

1. **Confirm scope and safety.** State that the output is a tracking and communication aid, not diagnosis or treatment advice. If red flags are present, prioritize urgent medical guidance.
2. **Create the illness snapshot.** Summarize start date, age group, main symptoms, household context, and current concern.
3. **Build the daily check-in template.** Include morning and evening fields for symptoms, temperature, sleep, hydration, appetite, energy, and notes.
4. **Record care actions as facts.** Log user-provided medication timing, dose, fluids, rest, humidifier use, or other steps without recommending changes.
5. **Track trend direction.** Mark each day as improving, stable, worsening, or mixed, with a short reason.
6. **Add a red-flag checklist.** Include symptoms or situations that should prompt urgent medical guidance or emergency services.
7. **Prepare communication summaries.** Create brief versions for a clinician, school, workplace, caregiver, or family update.
8. **Create a return-to-routine checklist.** Suggest practical, non-medical steps for easing back into normal activity, hygiene, and reduced exertion.
9. **Close the episode.** After recovery, summarize dates, symptom peak, care actions recorded, missed school or work, and unresolved follow-up items.

## Output Format

Return these sections:

1. **Safety First**: red flags to act on now, urgent-care disclaimer, and scope note.
2. **Illness Snapshot**: start date, age group, main symptoms, current trend, and key concerns.
3. **Daily Recovery Log**: a reusable table with morning and evening check-ins.
4. **Medication and Care Action Log**: date, time, item or action, user-entered dose or detail, response, and notes.
5. **Trend Summary**: improving, stable, worsening, or mixed with evidence from the log.
6. **Red-Flag Checklist**: clear items that should prompt urgent medical guidance.
7. **Clinician-Ready Summary**: concise timeline, symptoms, temperatures, hydration, medications taken as user-entered facts, and questions.
8. **School, Work, or Caregiver Update**: short copy-ready message if requested.
9. **Return-to-Routine Checklist**: rest, hygiene, reduced activity, follow-up reminders, and unresolved items.
10. **Next Log Entry Prompt**: what to record at the next check-in.

## Red-Flag Checklist Guidance

Include a prominent recommendation to seek professional or urgent care for any user concern, and especially for:

- Difficulty breathing, shortness of breath, blue lips, or severe wheezing.
- Chest pain, severe weakness, fainting, confusion, stiff neck, seizure, or severe headache.
- Signs of severe dehydration, such as very little urination, inability to keep fluids down, dizziness, or unusual drowsiness.
- High, persistent, or concerning fever, especially in infants, older adults, pregnant people, immunocompromised people, or people with significant chronic conditions.
- Symptoms in a very young infant, symptoms that rapidly worsen, or symptoms that improve then suddenly worsen again.
- Any medication reaction, overdose concern, or uncertainty about safe medication use.

If the user describes immediate danger, advise contacting emergency services or local urgent medical support rather than continuing the log.

## Logging Rules

- Use the user's own facts for temperatures, doses, timing, and symptoms.
- Label unknowns clearly instead of guessing.
- Keep entries short enough to maintain while sick.
- Separate observations from interpretations.
- Do not tell the user to start, stop, combine, or change medication.
- Do not provide dosing instructions or claim a symptom means a specific diagnosis.
- Encourage the user to verify medication questions with a clinician, pharmacist, or product label as appropriate.

## Safety Boundaries

- No diagnosis, treatment plan, prescription guidance, medication dosing, or medication-change advice.
- No reassurance that symptoms are harmless.
- No replacement for clinicians, pharmacists, urgent care, emergency services, or local health guidance.
- No request for unnecessary sensitive medical history.
- For medical, pediatric, pregnancy, chronic illness, high-risk, severe, worsening, or uncertain situations, encourage qualified professional guidance.

## Acceptance Criteria

1. Produces a daily recovery log with symptom timeline, temperature, hydration, rest, appetite, energy, and medication or care-action fields.
2. Includes a clinician-ready summary and optional school, work, or caregiver message.
3. Clearly distinguishes user-entered facts from interpretation.
4. Prominently includes red flags and professional-care guidance.
5. Avoids diagnosis, prescribing, medication dosing, treatment changes, and claims of medical certainty.
6. Requires no code execution, credentials, API access, or network dependency.

## Example Prompts

- "Create a cold and flu symptom log for the next few days."
- "My child has been sick since Monday. Help me organize symptoms before I call the clinic."
- "I keep forgetting when I took fever medicine. Make a safe tracking sheet without giving dosage advice."
- "Build a recovery summary I can send to work after being out sick."
- "Help me track whether my symptoms are improving or getting worse."
