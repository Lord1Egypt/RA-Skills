# Confidence Calibration

Decision confidence is about match quality, not bravado.

| Level | Meaning | Behavior |
|-------|---------|----------|
| **missing** | Key components are missing | Ask immediately |
| **partial** | Some components match, but important ones are unknown | Propose options, do not decide |
| **close** | Most components match a past decision, but one material factor differs | Ask with a recommendation |
| **validated** | Question and key components match a past confirmed decision | Safe to propose the stored answer |
| **confirmed-default** | User explicitly approved this exact component pattern as a default | May decide, then inform if stakes stay within the validated boundary |

## Rules

- Confidence rises only when the question and the material components both match.
- Repeated accuracy matters more than self-estimated certainty.
- A single contradiction or correction should demote confidence immediately.
- If the decision affects long-term architecture or irreversible cost, treat `validated` as ask-first unless the user explicitly promoted it to `confirmed-default`.

## Demotion Triggers

Demote the rule if:
1. The user chooses differently in the same situation
2. A previously ignored component turns out to change the answer
3. The project, client, budget, or platform differs materially
4. The user says the past rule was context-specific

**Default:** confidence should fail toward asking, not toward autonomy.
