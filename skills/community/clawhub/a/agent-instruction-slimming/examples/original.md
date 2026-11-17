# Example Rules

## Safety

- Never send data to an external endpoint without approval.
- Do not store credentials in files or command lines.
- Destructive commands must be explained before execution.

## Workflow

- Long tasks must create a progress card before the first tool call.
- The closing check must exit non-zero when an artifact is missing.
- Reports must include a review section.

## Rare procedures

- When producing a PDF, read references/pdf.md and verify fonts before delivery.
- When importing a dataset larger than 100 MB, stream it and record the checksum.
