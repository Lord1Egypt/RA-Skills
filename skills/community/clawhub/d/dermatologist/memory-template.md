# Memory Template - Dermatologist

Create `~/dermatologist/memory.md` with this structure:

```markdown
# Dermatologist Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation
- Use automatically when:
- Ask first when:
- Never activate for:

## Privacy Limits
- Storage approved: yes | no
- Photo tracking approved: yes | no
- Exports approved: yes | no
- Adults only tracking: yes
- Sensitive area restrictions:

## Clinician Context
- Preferred clinician or clinic:
- Upcoming visit date:
- Existing diagnoses confirmed by clinician:
- Pathology or biopsy history the user wants remembered:

## Case Index
- `case-id` - short label, body site, last update

## Notes
- Durable facts only.

---
*Updated: YYYY-MM-DD*
```

Create `~/dermatologist/cases/{case-id}/summary.md`:

```markdown
# Case Summary - {case-id}

- Concern:
- Body site:
- First noticed:
- Current status:
- User goal:
- Clinician-confirmed diagnosis:
- Last meaningful change:
```

Create `~/dermatologist/cases/{case-id}/timeline.md`:

```markdown
# Timeline - {case-id}

- YYYY-MM-DD - symptom change, spread, treatment change, clinician visit, or test result
```

Create `~/dermatologist/cases/{case-id}/photos.md`:

```markdown
# Photo Log - {case-id}

| Date | File or source | Body site | View | Conditions | Comparison note |
|------|----------------|-----------|------|------------|-----------------|
```

Create `~/dermatologist/cases/{case-id}/treatment-log.md`:

```markdown
# Treatment Log - {case-id}

| Start | Stop | Product or medication | Purpose | Frequency | Effect | Irritation or issues |
|-------|------|-----------------------|---------|-----------|--------|----------------------|
```

Create `~/dermatologist/cases/{case-id}/consult-notes.md`:

```markdown
# Consult Notes - {case-id}

## Questions
- 

## Visit Outcome
- Date:
- Clinician said:
- Tests or biopsy:
- Next step:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning how the user tracks skin concerns | ask only high-impact follow-ups |
| `complete` | tracking system is stable | reuse saved structure and language |
| `paused` | storage is paused | read-only if already approved |
| `never_ask` | user does not want storage | avoid future storage prompts |

## Key Principles

- Keep hot memory short and use per-case folders for details.
- Save only confirmed facts or clearly attributed user statements.
- Separate clinician-confirmed diagnosis from model language.
- Use dates on every meaningful change, treatment, and visit.
- Never create image-tracking records for minors or intimate areas.
- Support delete and export workflows without friction.
