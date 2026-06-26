---
name: Dermatologist
slug: dermatologist
version: 1.0.0
homepage: https://clawic.com/skills/dermatologist
description: Track skin lesions, rashes, photos, treatment response, and dermatology visit prep with conservative triage, case-based records, and privacy guardrails.
changelog: "Initial release with case-based skin tracking, photo comparison, treatment logs, consultation prep, and privacy-first legal guardrails."
metadata: {"clawdbot":{"emoji":"D","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/dermatologist/"]}}
---

## When to Use

Use when the user needs skin-photo comparison, case tracking, treatment-response logging, or dermatologist visit prep. This is for conservative triage and documentation, not prescribing.

## Architecture

Memory lives in `~/dermatologist/`. If `~/dermatologist/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/dermatologist/
├── memory.md
├── cases/
│   └── {case-id}/
│       ├── summary.md
│       ├── timeline.md
│       ├── photos.md
│       ├── treatment-log.md
│       └── consult-notes.md
└── exports/
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Urgency triage | `triage.md` |
| New-case intake | `intake.md` |
| Compact red-flag checklist | `red-flags.md` |
| Standardized photo capture | `photo-protocol.md` |
| Case naming and evolution | `tracking.md` |
| Treatment and trigger logging | `treatment-log.md` |
| Consultation prep and follow-up | `consult-prep.md` |
| Visit-summary export pattern | `consult-workflow.md` |
| Legal and privacy guardrails | `legal-boundaries.md` |

## Scope

This skill ONLY:
- organizes skin concerns, photos, timelines, exposures, and visit prep
- stores local records in `~/dermatologist/` if the user approves
- gives conservative escalation guidance for clinician follow-up

This skill NEVER:
- diagnose skin cancer, melanoma, infections, autoimmune disease, or drug reactions from chat or photos alone
- prescribe medication, dosing, biopsy decisions, or treatment escalation without a clinician
- ask for or store intimate-area images or any photos of minors
- upload photos or health data to external services
- present itself as a licensed clinician or substitute for in-person care

## Security & Privacy

**Data that leaves your machine:**
- None.

**Data stored locally if approved by the user:**
- activation preference and privacy choices in `~/dermatologist/memory.md`
- one case folder per skin concern with dated notes, photo metadata, and treatment logs
- visit summaries in `~/dermatologist/exports/`

**This skill does NOT:**
- upload images or call undeclared services
- infer identity or diagnosis from a photo
- create reminders or automations automatically
- replace clinician judgment, pathology, biopsy, or emergency care

## External Endpoints

This skill makes no external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Core Rules

### 1. Triage Before Skin Theory
- Open `triage.md` before giving pattern guesses or tracking advice.
- Use `red-flags.md` when urgency needs a shorter checklist.
- Rule out emergency, same-day, and urgent in-person care first.

### 2. Keep One Case Per Concern
- Use one folder per lesion, rash episode, or stable body-site problem.
- Use `intake.md` to capture the first high-signal questions.
- If the morphology, body area, or time course differs, split into a new case instead of merging.

### 3. Standardize Photos Before Comparing
- Use `photo-protocol.md` for lighting, angle, scale, and naming.
- Prefer the same room, distance, body position, and camera whenever possible.
- Do not claim change when the photo conditions are too different.

### 4. Separate Facts, Impressions, and Clinician Statements
- Record what the user reports, what is visible under a limited description, and what a clinician said as separate buckets.
- Offer differentials as possibilities to discuss, not as conclusions.

### 5. Log Exposures and Treatment Response With Dates
- Use `treatment-log.md` to track products, prescriptions, triggers, and adherence.
- Capture dates, frequency, missed doses, irritation, itch, pain, bleeding, and meaningful exposures.

### 6. Prepare Consultations Like a Specialist Handoff
- Use `consult-prep.md` to compress onset, evolution, failed treatments, triggers, and exact questions.
- Use `consult-workflow.md` when the user wants an export-ready visit summary.
- Surface the smallest set of facts that changes clinician decision-making.

### 7. Privacy and Legal Boundaries Outrank Convenience
- Use `legal-boundaries.md` whenever storage, sharing, or productization comes up.
- Ask before writing local files or saving photo metadata.
- If minors or intimate-area images appear, stop image collection and redirect to in-person or secure clinician workflows.
- If the user is building a patient-facing product, require jurisdiction-specific legal review before deployment.

## Common Traps

- Comparing photos with different lighting, zoom, or camera modes -> fake progression.
- Mixing acne, mole tracking, scalp symptoms, and a sudden rash into one timeline -> unusable record.
- Treating words like "itchy," "red," or "raised" as a diagnosis -> overclaiming from low-signal inputs.
- Suggesting "watch and wait" with bleeding, fast change, fever, eye involvement, mucosal lesions, or severe pain -> unsafe delay.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `doctor` - general medical boundaries when a skin issue may reflect broader illness
- `health` - broader symptom framing outside specialty care
- `memory` - persistent local memory for long-running follow-up
- `photos` - broader photo organization workflows beyond dermatology tracking

## Feedback

- If useful: `clawhub star dermatologist`
- Stay updated: `clawhub sync`
