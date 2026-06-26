# Memory Template - Dog

Create `~/dog/memory.md` with this structure:

```markdown
# Dog Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Household Summary
- Dogs in home:
- Shared constraints:
- Walk coverage:
- Emergency preference:

## Activation
- Use automatically when:
- Ask first when:
- Never activate for:

## Shared Red Flags
- Signal:
- Why it matters:

## Notes
- Durable observations only.

---
*Updated: YYYY-MM-DD*
```

Create `~/dog/dogs/{name}/profile.md` with this structure:

```markdown
# {Name}

## Identity
- Age or range:
- Sex:
- Breed or type:
- Weight range:
- Microchip:

## Health Baseline
- Conditions:
- Allergies:
- Medications:
- Normal appetite:
- Normal stool and urine:

## Training and Handling
- Recall level:
- Walk setup:
- Trigger list:
- Handling limits:
- Best rewards:
```

Create `~/dog/dogs/{name}/timeline.md` with short dated facts:

```markdown
# Timeline - {Name}

- YYYY-MM-DD - symptom change, appointment, training milestone, incident, or memorable event
```

Create `~/dog/shopping.md` with shared supplies:

```markdown
# Dog Supplies

| Item | Normal brand or type | Reorder point | Notes |
|------|----------------------|---------------|-------|
| Food | | | |
| Treats | | | |
| Medication | | | |
| Waste bags | | | |
| Grooming items | | | |
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning the household | ask only high-impact follow-ups |
| `complete` | core context is stable | act faster using saved defaults |
| `paused` | memory use paused | read-only if already approved |
| `never_ask` | no setup prompts | avoid future setup questions |

## Key Principles

- Keep hot memory short and household-level.
- Store per-dog facts in that dog's folder, not in the shared file.
- Save only confirmed or clearly attributed observations.
- Use dates for symptom changes, meds, appointments, incidents, and milestones.
- Remove stale guesses once the user or vet clarifies the situation.
