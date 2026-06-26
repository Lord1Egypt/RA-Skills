# Consistency Review

Run this review after section drafting and before DOCX finalization.

## Purpose

A strong draft can still fail if the document disagrees with itself. This review is about cross-section coherence, not sentence polishing.

## Review checklist

Check these items across the whole document:

- Terminology: same thing, same name.
- Scope: the same boundaries appear in every relevant section.
- Quantities: counts, mileage, locations, and capacities do not drift.
- Interfaces: upstream, downstream, and external systems match across chapters.
- Roles and responsibilities: no contradictory ownership.
- Standards and references: clause numbers and standard names are consistent.
- Numbering: heading and figure/table numbering are continuous.
- Tone: no section falls into a different style or audience unexpectedly.

## Collision patterns

Look for these common failures:

- The same content appears in both design and implementation sections with different wording.
- A management chapter promises a timeline that the technical chapter cannot support.
- A security or quality chapter introduces requirements absent from the technical scope.
- A final chapter still exposes working-source labels or draft-stage notes.

## Resolution order

1. Fix factual contradictions.
2. Fix boundary and ownership collisions.
3. Fix numbering and naming.
4. Fix style-level inconsistencies.

## Deliverable split

When helpful, produce two artifacts:

- A clean merged draft.
- A short review memo listing contradictions fixed, assumptions kept, and items that still need user confirmation.
