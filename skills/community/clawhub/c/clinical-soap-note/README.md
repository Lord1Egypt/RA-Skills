# Clinical SOAP Note Drafter

**Platforms:** Claude · Codex
**Domain:** Healthcare

## Purpose

Turns a clinician's raw encounter notes, dictation, or bullet points into a structured SOAP note draft (Subjective / Objective / Assessment / Plan) with explicit gap flags and coding prompts. Reduces the documentation time clinicians spend manually structuring notes, while keeping a licensed clinician fully in the loop.

## When to Use

- After a patient encounter when dictation or rough notes must become a structured visit note
- When converting bullet fragments into a consistent SOAP layout
- When a scribe needs a first-pass draft for clinician review and sign-off
- When a partial note needs organizing without inventing missing content

## What It Does

**Phase 1: Intake**
1. Collects encounter type, specialty context, and the raw material — one question at a time

**Phase 2: Structuring**
2. Classifies the input (narrative, bullets, or partial note) and maps every supplied detail into exactly one SOAP section
3. Flags commonly expected but missing information instead of fabricating it

**Phase 3: Output**
4. Produces a SOAP draft with `[FLAG]` items, non-binding coding prompts, a consolidated unresolved-items list, and a mandatory clinician-review notice

## Safety

- Never gives medical advice, diagnoses, or treatment recommendations
- Never fabricates clinical findings, vitals, labs, or history
- Treats all input as PHI: no storage, external transmission, or reuse beyond the session
- Output is always a draft requiring licensed clinician verification and signature before any clinical or billing use

## Notes

This skill is a documentation drafting aid only. It does not replace clinical judgment and produces nothing that can be entered into a medical record without clinician review.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.