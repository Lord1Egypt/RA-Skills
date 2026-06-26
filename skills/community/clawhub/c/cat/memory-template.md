# Memory Template - Cat

Create `~/cat/memory.md` with this structure:

```markdown
# Cat Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Household Summary
- Cats in home:
- Indoor or outdoor:
- Shared constraints:
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

Create `~/cat/cats/{name}/profile.md` with this structure:

```markdown
# {Name}

## Identity
- Age or range:
- Sex:
- Breed or type:
- Microchip:
- Adoption date:

## Health Baseline
- Conditions:
- Allergies:
- Medications:
- Normal appetite:
- Normal litter pattern:

## Handling and Environment
- Carrier tolerance:
- Handling limits:
- Favorite food:
- Favorite play:
- Stress triggers:
```

Create `~/cat/cats/{name}/timeline.md` with short dated facts:

```markdown
# Timeline - {Name}

- YYYY-MM-DD - symptom change, appointment, milestone, or memorable event
```

Create `~/cat/shopping.md` with shared supplies:

```markdown
# Cat Supplies

| Item | Normal brand or type | Reorder point | Notes |
|------|----------------------|---------------|-------|
| Wet food | | | |
| Dry food | | | |
| Litter | | | |
| Medication | | | |
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
- Store per-cat facts in that cat's folder, not in the shared file.
- Save only confirmed or clearly attributed observations.
- Use dates for symptom changes, meds, appointments, and milestones.
- Remove stale guesses once the user or vet clarifies the situation.
