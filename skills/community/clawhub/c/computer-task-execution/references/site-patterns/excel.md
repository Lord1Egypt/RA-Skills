---
kind: local-app
name: Microsoft Excel
aliases: [Excel, Microsoft Excel]
updated: 2026-03-27
---

## Platform traits
- Excel tasks split into structured edits and layout-sensitive GUI edits.
- Pure GUI editing is not the default if the same result can be achieved more deterministically by structured operations.

## Successful paths
- [2026-03-27] Structured-edit flow: identify workbook/sheet/range → prepare intended changes in advance → apply edits in the most direct available way → read back changed cells or sheet state.
- [2026-03-27] GUI-edit flow: prepare all edits first → focus Excel → navigate directly to the target sheet/range → perform the shortest possible foreground edit sequence → reread or visually confirm result.

## Preconditions
- Workbook is accessible.
- Target sheet/range can be identified.
- The requested change type is understood before entering the GUI.

## Verification
- Read back changed cells/sheet state after edit.
- Use visible confirmation for formatting/layout-sensitive results.

## Unstable or failed paths
- [2026-03-27] Long foreground editing sessions are less preferred than batch-prepared edits with short execution windows.
- [2026-03-27] Background-only keyboard control is not reliable unless previously proven for the exact flow.

## Recommended default
- Prefer structured/scriptable edits first.
- Use local GUI execution only for layout-sensitive or app-specific tasks.

## Notes for future runs
- Separate “data change” from “layout/view change” before choosing the execution path.
