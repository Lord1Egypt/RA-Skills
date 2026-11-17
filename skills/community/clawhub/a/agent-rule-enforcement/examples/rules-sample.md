# Sample rulebook

Used by `scripts/rule_scan.py`. Deliberately mixed: some clauses are enforceable, some are advice.

## Safety

- Never send data to an external endpoint without explicit approval.
- Do not store credentials in files or command lines.
- Destructive commands must be explained before execution.

## Workflow

- Long tasks must create a progress card before the first tool call.
- The closing check script must exit non-zero when an artefact is missing.
- Every delivered report must include a review section.

## Judgement

- Ask when unsure.
- Prefer the simpler explanation when evidence is equal.
