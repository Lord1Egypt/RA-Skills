---
kind: local-app
name: Microsoft PowerPoint
aliases: [PowerPoint, Microsoft PowerPoint, PPT]
updated: 2026-03-27
---

## Platform traits
- PowerPoint tasks often depend on visible slide state, so visual verification matters.
- Prefer object/template/file-level edits when the request does not require live canvas inspection.

## Successful paths
- [2026-03-27] Structured-edit flow: identify presentation/slide/object target → prepare intended edits first → apply direct/object-level changes where possible → verify by rereading object state or slide result.
- [2026-03-27] Visual-layout flow: prepare edit intent → focus PowerPoint → navigate directly to target slide/object → perform the shortest possible foreground change sequence → visually verify the resulting slide.

## Preconditions
- Presentation is accessible.
- Target slide/object can be identified.
- The edit can be scoped before entering the GUI.

## Verification
- Read back slide/object state if available.
- Use visible slide confirmation for layout-sensitive changes.

## Unstable or failed paths
- [2026-03-27] Background-only UI control is not the default for layout-heavy work.
- [2026-03-27] Repeated manual-style navigation is less preferred than direct target selection plus focused edit execution.

## Recommended default
- Prefer structured edits first.
- Use local GUI only when visible slide state is part of the success criteria.

## Notes for future runs
- If success depends on what the slide looks like, visual verification is mandatory.
