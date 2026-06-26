# AANA Medical Safety Router Skill

Use this skill when an OpenClaw-style agent may answer, summarize, triage, draft, or route a medical, health, wellness, medication, symptom, diagnosis, treatment, nutrition, mental health, fitness, or safety-related question.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Medical and wellness replies should stay inside safer boundaries: acknowledge uncertainty, avoid diagnosis overclaims, route emergencies, encourage appropriate clinician involvement, and avoid exposing private health information.

The agent should separate:

- general health education,
- user-reported symptoms,
- verified medical facts available in context,
- missing context that affects safety,
- emergency or urgent warning signs,
- diagnosis, treatment, prescription, dosage, or clinical decision claims,
- private health information that should be minimized.

## When To Use

Use this skill before replying to:

- symptom, illness, injury, medication, dosage, side effect, treatment, diagnosis, lab result, or condition questions,
- mental health, self-harm, crisis, eating disorder, addiction, or abuse-related questions,
- pregnancy, child health, elderly care, disability, or chronic disease questions,
- diet, supplement, exercise, sleep, wellness, or fitness advice with health implications,
- requests to interpret medical records, images, labs, prescriptions, or clinician notes,
- requests to choose between treatments, stop medication, change dosage, or delay care.

## Medical Risk Classes

Treat these as higher risk:

- emergency symptoms such as chest pain, severe trouble breathing, stroke-like symptoms, severe allergic reaction, major injury, poisoning, overdose, seizure, suicidal intent, or sudden severe neurological symptoms,
- medication, dosage, interactions, pregnancy, pediatrics, elderly patients, chronic conditions, immunocompromise, or post-surgery issues,
- diagnosis or treatment selection,
- medical images, lab results, genetic results, pathology, radiology, or clinician notes,
- mental health crisis, self-harm, harm to others, abuse, neglect, or unsafe living conditions,
- private health information, insurance, billing, legal, employment, or school accommodation context.

## AANA Medical Routing Loop

1. Identify the user request and the health-related decision it may influence.
2. Classify the response type: general education, wellness guidance, symptom triage, medication question, diagnosis request, treatment request, emergency, or crisis.
3. Check emergency signs: route urgent or potentially life-threatening scenarios to emergency services or immediate medical care.
4. Check diagnosis overclaiming: do not state or imply a definitive diagnosis from limited chat context.
5. Check treatment overclaiming: do not prescribe, change dosage, stop medication, or replace clinician judgment.
6. Check uncertainty: state limits clearly when symptoms, records, or context are incomplete.
7. Check referral: recommend clinician, pharmacist, emergency care, crisis support, or local qualified professional when needed.
8. Check privacy: minimize private health details and avoid unnecessary repetition of sensitive information.
9. Choose action: accept, revise, ask, retrieve, defer, emergency_route, crisis_route, or refuse.

## Emergency Routing

If the user describes urgent warning signs, do not continue with routine advice. Tell them to seek immediate emergency help now, such as local emergency services or the nearest emergency department.

Urgent warning signs include:

- chest pain, severe shortness of breath, fainting, severe weakness,
- stroke-like symptoms: face drooping, arm weakness, speech trouble, sudden confusion,
- severe allergic reaction, swelling of face or throat, trouble breathing,
- major bleeding, serious head injury, severe burns, poisoning, overdose,
- seizure, sudden severe headache, stiff neck with fever,
- suicidal intent, intent to harm others, or inability to stay safe,
- symptoms in infants, pregnancy, elderly, immunocompromised, or post-surgery patients that may be urgent.

Use direct language:

```text
This could be urgent. Please seek emergency medical help now or contact local emergency services.
```

## Diagnosis Boundary

Do not say:

- "You have..."
- "This is definitely..."
- "That rules out..."
- "You do not need medical care..."
- "It is safe to ignore..."

Prefer:

- "I cannot diagnose this from chat."
- "Several causes are possible."
- "A clinician can evaluate this with an exam and tests."
- "If symptoms are severe, worsening, or new, seek urgent care."

## Medication And Treatment Boundary

Do not:

- prescribe medication,
- change dosage,
- tell a user to stop prescribed medication,
- promise safety of drug combinations,
- interpret medication interactions as definitively safe,
- replace a clinician or pharmacist.

Prefer:

- "Check with your prescribing clinician or pharmacist before changing this."
- "If you already took it and feel unwell, seek medical advice promptly."
- "I can help list questions to ask your clinician."

## Wellness Boundary

For low-risk wellness questions, give general information and encourage personalization:

- avoid claims that a diet, supplement, exercise, or sleep routine treats or cures disease,
- note that needs vary by age, pregnancy, conditions, medications, and injury history,
- recommend starting gently and stopping if concerning symptoms appear,
- refer to a qualified professional for medical conditions or persistent symptoms.

## Private Health Data Rules

Minimize or remove:

- diagnoses, symptoms, medications, lab results, insurance details, appointments,
- clinician notes, mental health details, disability status, pregnancy details,
- family history, genetic information, images, private messages, and identifiers.

Do not include raw health records, full medical notes, insurance identifiers, or another person's health information unless necessary and authorized.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `medical_context`
- `risk_level`
- `emergency_status`
- `diagnosis_overclaim_status`
- `treatment_overclaim_status`
- `privacy_status`
- `recommended_action`

Do not include raw medical records, images, lab reports, insurance details, private messages, credentials, or full clinician notes when a redacted summary is enough.

## Decision Rule

- If the question is low-risk and answerable as general education, accept with uncertainty and appropriate boundaries.
- If the draft overdiagnoses, overtreats, or implies certainty beyond evidence, revise.
- If key context is missing and the situation is not urgent, ask.
- If clinician, pharmacist, crisis, or emergency care is needed, defer or route.
- If the request asks for unsafe instructions, hidden self-harm help, or evasion of medical care in a dangerous situation, refuse unsafe parts and route to appropriate help.
- If a checker is unavailable or untrusted, use manual medical-safety review.

## Output Pattern

For medical-sensitive replies, prefer:

```text
Medical safety review:
- Risk level: ...
- Emergency signs: ...
- Diagnosis boundary: ...
- Treatment boundary: ...
- Referral: ...
- Privacy: ...
- Decision: accept / revise / ask / defer / emergency_route / crisis_route / refuse
```

Do not include this review block in the user-facing answer unless the support or safety workflow requires it.
