# Manual Policy

Use this reference when a task depends on BMW factory procedures, values, diagrams, or service data.

## Allowed

- Ask the user to consult their own legally obtained BMW Repair Manual PDF.
- Interpret short user-provided excerpts, notes, measurements, photos, and page references.
- Build checklists that point back to manual sections the user already has.
- Summarize user-provided content without reproducing full manual sections.

## Not Allowed

- Include the BMW Repair Manual PDF in this repository.
- Reproduce factory manual chapters, scanned pages, diagrams, torque tables, wiring tables, or proprietary service schedules.
- Invent exact BMW specifications when the manual has not been supplied.
- Tell the user to ignore BMW warnings or sequence requirements.

## Practical Prompt

When factory information is missing, say:

```text
Please open your legally obtained BMW Repair Manual PDF and provide the relevant page, section title, or a short excerpt for the exact specification or procedure. I can then help interpret it and turn it into a safe checklist.
```
